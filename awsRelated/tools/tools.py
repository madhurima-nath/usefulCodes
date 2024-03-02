from abc import ABC
from langchain_core.tools import BaseTool

class BedrockTool(BaseTool, ABC):
    anthropic_function: str
    """XML description of the function that will ne passed to the LLM"""


class GetAvailableGroups(BedrockTool):
    """Tool that retrieve available groups"""

    name: str = "get_available_groups"
    description: str = (
        "return available group ids. "
        "this tool does not take any input"
        "the output of the tool will be a comma separated string "
        "with available group ids"
    )
    anthropic_function: str = (
        "<tool_description>"
        f"<tool_name>{name}</tool_name>"
        f"<description>{description}</description>"
        "</tool_description>"
    )
    processed_file: dict

    def __init__(self, processed_file: dict):
        super().__init__(processed_file=processed_file)

    def _run(self) -> str:
        return ",".join(list(self.processed_file.keys()))
    

class GetPrevalenceTool(BedrockTool):
    """Tool that retrieve probability values of groups"""

    name: str = "get_probabilities"
    description: str = (
        "Retrieve probability information of groups. "
        "The input of this tool should be a comma separated list "
        "of group ids coming from get_available_groups tool."
        "The output of the tool will provide"
        "First, inside the <probability></probability> tags, "
        "you will get the feature name and probability value "
        "of each group in the input parameters."
        "Second, inside the <feature description> </feature description> tags "
        "you will find feature descriptions that will give extra context "
        "to how those features were constructed."
    )
    anthropic_function: str = (
        "<tool_description>"
        f"<tool_name>{name}</tool_name>"
        f"<description>{description}</description>"
        "</tool_description>"
        "<parameters>"
        "<parameter>"
        "<name>group_ids</name>"
        "<type>string</type>"
        "description>Comma separated list of group ids.</description>"
        "</parameter>"
        "</parameters>"
        "<description>key-value pair list of features and descriptions.</description>"
    )
    processed_file: dict

    def __init__(self, processed_file: dict)
        super().__init__(
            processed_file=processed_file
        )

    def _search(self, group_ids: list) -> str:
        output = ""

        for group in group_ids:
            output += f"<probability id = '{group}'>" + "\n"

            for idx, (feature, val) in enumerate(
                self.processed_file.get(group)
            ):
                output += f"<feature id='{idx}'>{feature} = {val}</feature>\n"
            output += f"</probability>" + "\n"

            feature_list = [
                feature for feature, _ in self.processed_file.get(group_ids[0])
            ]
            for idx, feature in enumerate(feature_list):
                desc = self.processed_file.get(feature, "-1")
                output += (
                    f"<feature id='{idx}'>Definition of {feature} is '{desc}'
                    </feature>\n"
                )
            output += "</feature description>"

            return output
        

class GetSortedGroups(BedrockTool):
    """Tool that sorts available groups"""

    name: str = "sort_available_groups"
    description: str = (
        "This tool takes an input column id which "
        "is a string and returns a string SUCCESS "
        "when the tool executes successfully or "
        "FAILURE otherwise."
    )
    anthropic_function: str = (
        "<tool_description>"
        f"<tool_name>{name}</tool_name>"
        f"<description>{description}</description>"
        "</tool_description>"
        "<parameters>"
        "<parameter>"
        "<name>column</name>"
        "<type>string></type>"
        "<description>String representing a column id.</description>"
        "</parameter>"
        "</parameters>"
    )

    def _run(self, column_id) -> str:
        return "<answer>SUCCESS</answer>"