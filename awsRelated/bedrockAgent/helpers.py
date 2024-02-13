from typing import List, Tuple
from tools.tools import BedrockTool
from langchain_core.agents import AgentAction

def format_xml(
        intermediate_steps: List[Tuple[AgentAction, str]]
) -> str:
    """
    Format the intermediate steps as XML.

    Args:
        intermediate_steps: the intermediate steps.

    Returns:
        the intermediate steps as XML.
    """
    log = ""
    for action, observation in intermediate_steps:
        # get start and end of XML function call
        start = action.log.find("<function_calls")
        end = action.log.find("</function_calls") + len("</function_calls>")

        # extract XML string
        log += action.log[start:end] + "\n"
        log += (
            "<function_results>"
            f"<tool_name>{action.tool}</tool_name>"
            f"<parameters>{action.tool}</parameters>"
            f"<stdout>{action.tool}</stdout>"
        )
    return log

def get_tools_string(tools: List[BedrockTool]) -> str:
    return "<tools>" + "".join([elt.anthropic_function for elt in tools]) + "</tools>"