from typing import List, Union

import xml.etree.ElementTree as ElementTree

from langchain_core.agents import (
    AgentAction, AgentActionMessageLog, AgentFinish,
)
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
)
from langchain_core.outputs import ChatGeneration, Generation
from langchain.agents.agent import AgentOutputParser

class BedrockFunctionsAgentOutputParser(AgentOutputParser):
    @staticmethod
    def _extract_function_call(full_text):
        if "function_calls" not in full_text:
            # XML tag wasn't found in the agent response.
            # can't extract function call
            return None
        
        # get start and end of the first XML function call
        start = full_text.find("<function_calls>")
        if "</function_calls>" in full_text:
            # truncating the string to get the first function call only
            end = full_text.find("</function_calls>") + len("</function_calls>")
            xml_string = full_text[start:end]
        else:
            # agent output was truncated by the </funcation_call> stop sequence
            # we are taking the entire response
            xml_string = full_text[start:] + "</function_calls>"

        # extract xml string
        root = ElementTree.fromstring(xml_string)

        # get the tool name
        tool_name = root.find(".//tool_name").text

        # extract parameters
        parameters = {}
        for param in root.findall(".//parameters/*"):
            parameters[param.tag] = param.text

        # return structured dictionary based on xml function call
        return {"name": tool_name, "arguments": parameters}
    

    @property
    def _type(self) -> str:
        return "bedrock-functions-agent"
    
    def _parse_ai_message(
            self, message: BaseMessage
    ) -> Union[AgentAction, AgentFinish]:
        """parse an AI message"""
        if not isinstance(message, AIMessage):
            raise TypeError(f"Expected an AI message got {type(message)}")
        
        function_call = self._extract_function_call(message.content)

        if function_call:
            function_name = function_call["name"]
            try:
                # try using the logic the LLM suggested
                tool_input = function_call["arguments"]
            except Exception:
                raise OutputParserException(
                    f"Could not parse tool input: {function_call} because "
                    f" the `arguments` is not valid XML syntax."
                )
            
            content_msg = (
                f"LLM response: {message.content}\n" if message.content else "\n"
            )
            log = (
                f"{content_msg}\n" f"Invoking: `{function_name}` with {tool_input}`\n"
            )
            return AgentActionMessageLog(
                tool=function_name,
                tool_input=tool_input,
                log=log,
                message_log=[message]
            )
        else:
            # no function call
            # this is the final result from the agent
            return AgentFinish(
                return_values={"output": message.content},
                log=str(message.content)
            )
    
    def parse_result(
            self, result: List[Generation], *, partial: bool = False
    ) -> Union[AgentAction, AgentFinish]:
        if not (
            isinstance(result[0], ChatGeneration) or isinstance(result[0], Generation)
        ):
            raise ValueError(
                "This output parser only works on ChatGeneration or Generation output"
            )
        message = result[0].message
        return self._parse_ai_message(message)
    
    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        raise ValueError("Can only parse messages")

