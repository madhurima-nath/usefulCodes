import yaml
from langchain_community.chat_models.bedrock import BedrockChat
from agent.AgentExecutorBatch import AgentExecutorBatch
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from agent.helpers import format_xml, get_tools_string
from agent.BedrockFunctions import BedrockFunctionsAgentOutputParser
from agent.prompt_templates import (
    PROMPT_TEMPLATE,
    HUMAN_TEMPLATE,
    FUNCTION_CALLING_PROMPT_TEMPLATE,
)
from tools.tools import GetPrevalenceTool, GetAvailableGroups # user-defined modules
from preprocess import DataProcess # user-defined module for preprocessing

class ConfigParser:
    """
    reads configuartion from config.yaml
    """
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def load_parameters(config_path: str = "config.yaml") -> dict:
        """
        loads parameters from YAML file
        :param config_path: (str, optional) - path to config file
        :return: (dict) dictionary of parameters
        """
        with open(config_path, "r") as file:
            config_yaml = yaml.safe_load(file)
        return config_values
    
def get_bedrock_llm(**kwargs):
    return BedrockChat(
        credentials_profile_name=kwargs.get("credentials_profile_name"),
        region_name=kwargs.get("region_name"),
        model_id=kwargs.get("model_id"),
        model_kwargs=kwargs.get("model_kwargs"),
    )

def get_chain(**kwargs):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", PROMPT_TEMPLATE),
            ("human", HUMAN_TEMPLATE),
        ]
    )
    llm = get_bedrock_llm(**kwargs)
    return prompt | llm

def get_agent(llm, tools, return_intermediate_steps=True, verbose=True):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", PROMPT_TEMPLATE + FUNCTION_CALLING_PROMPT_TEMPLATE),
            ("human", "{input}"),
            ("assistant", "{agent_scratchpad}"),
        ]
    )

    agent = (
        RunnablePassthrough.assign(
            agent_scratchpad = lambda x: format_xml(x["intermediate_steps"])
        )
    | prompt
    | llm
    | BedrockFunctionsAgentOutputParser()
    )
    return AgentExecutorBatch(
        agent=agent,
        tools=tools,
        verbose=verbose,
        return_intermediate_steps=return_intermediate_steps,
    )

def main(question: str, file_path: str = None) -> dict:
    """
    main entrypoint to langchain agent and generate a response to the user `question`

    :param question: string - User question that will be sent to the LLM
        through the defined langchain agent
    :param file_path: string - AWS URI to the JSON file that will be passed
        as context to the LLM e.g. "bucket-name/folder/foo.json"
        N.B: URI needs to be in S3 bucket in the `config.yaml` parameter
    :return: dictionary - Dictionary containing the LLM answer in the `output` key
        Dictionary wull have the following tags:
            `input`: question sent to the model
            `tools_string`: tools sent to the agent
            `output`: answer
    """

    parser = ConfigParser()
    config = parser.load_parameters()

    aws_config = config.get("aws_configuration")
    if file_path:
        aws_config["file_path"] = file_path
    local_preprocessing_config = config.get("local_preprocessing_configuration")

    data_process = DataProcess(aws_config, local_preprocessing_config)
    data_process.download_files()
    data_process.filepreprocess()
    preprocessed_file = data_process.get_preprocessed_data()

    agent_tools = [
        GetPrevalenceTool(preprocessed_file),
        GetAvailableGroups(preprocessed_file),
    ]
    llm = get_bedrock_llm(**aws_config)

    agent_executor = get_agent(
        llm, agent_tools, return_intermediate_steps=False, verbose=False
    )

    return agent_executor.invoke(
        {"input": question, "tools_string": get_tools_string(agent_tools)}
    )

if __name__ == "__main__":
    user_question = (
        "Provide a short description and propose a name for group"
    )
    answer = main(user_question)
    print(answer.get("output"))
    