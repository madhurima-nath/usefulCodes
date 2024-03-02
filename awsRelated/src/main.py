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
from tools.tools import ( # user-defined modules
    GetPrevalenceTool, 
    GetAvailableGroups,
    GetSorteGroups,
)
# user-defined module for preprocessing
from preprocess.dataProcess import DataProcess 



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


def name_group_chain(llm):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", PROMPT_TEMPLATE + NAME_GROUP_RULES),
            (
                "human",
                "{context}\n\n Question: Propose a name that summarizes each group",
            ),
        ]
    )
    return prompt | llm


# def get_chain(**kwargs):
#     prompt = ChatPromptTemplate.from_messages(
#         [
#             ("system", PROMPT_TEMPLATE),
#             ("human", HUMAN_TEMPLATE),
#         ]
#     )
#     llm = get_bedrock_llm(**kwargs)
#     return prompt | llm


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


def read_config_and_execute_preprocess(datapath: str = None) -> (dict, dict):
    parser = ConfigParser()
    config = parser.load_parameters()

    aws_config = config.get("aws_configuration")
    if datapath:
        aws_config["raw_json_path"] = datapath
    local_filepath_config = config.get("local_filepath_configuration")

    data_process = DataProcess(aws_config, local_filepath_config)
    data_process.download_files()
    data_process.file_preprocess()
    processed_file = data_process.get_processed_data()
    return config, processed_file


def answer_query(question: str, datapath: str = None) -> dict:
    """
    entrypoint to langchain agent and generate a response to the user `question`

    :param question: string - User question that will be sent to the LLM
        through the defined langchain agent
    :param datapath: string - AWS URI to the JSON file that will be passed
        as context to the LLM e.g. "bucket-name/folder/foo.json"
        N.B: URI needs to be in S3 bucket in the `config.yml` parameter
    :return: dictionary - Dictionary containing the LLM answer in the `output` key
        Dictionary will have the following tags:
            `input`: question sent to the model
            `tools_string`: tools sent to the agent
            `output`: answer
    """
    (
        config,
        processed_file,
    ) = read_config_and_execute_preprocess(datapath)

    agent_tools = [
        GetAvailableGroups(processed_file),
        GetPrevalenceTool(processed_file),
        GetSortedGroups(),
    ]

    llm = get_bedrock_llm(**config.get("aws_configuration"))

    agent_executor = get_agent(
        llm,
        agent_tools,
        return_intermediate_steps=False,
        verbose=False,
    )

    return agent_executor.invoke(
        {"input": question, "tools_string": get_tools_string(agent_tools)}
    )


def name_groups(datapath: str = None) -> str:
    """
    entrypoint to langchain agent.
    generates description for each group in the json file passed as context.

    :param datapath: string - AWS URI to the JSON file that will be passed
        as context to the LLM e.g. "bucket-name/folder/foo.json"
        N.B: URI needs to be in S3 bucket in the `config.yml` parameter
    :return: str - LLM answer. each group name should be in its own
        XML tag following the <group K> format where K is the group id.
    """
    (
        config,
        processed_file,
    ) = read_config_and_execute_preprocess(datapath)

    llm = get_bedrock_llm(**config.get("aws_configuration"))

    chain = name_group_chain(llm)

    tool = GetPrevalenceTool(processed_file)
    context = tool(",".join(processed_file.keys()))
    return chain.invoke({"context": context}).content


if __name__ == "__main__":
    user_question = (
        "Provide a short description and propose a name for group"
    )
    answer = main(user_question)
    print(answer.get("output"))
    