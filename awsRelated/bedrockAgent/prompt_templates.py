PROMPT_TEMPLATE = """
You are an <insert character of the bot> desgined to answer
user questions on <topics to answer questions>.
<Provide context of the task and the topic.>
Look at the additional context below to understand the result
of the analysis and then help answer the user questions.
"""

HUMAN_TEMPLATE = """
=== BEGIN CONTEXT ===
{details}
=== END CONTEXT ===

=== BEGIN CONTEXT ===
{details}
=== END CONTEXT ===

question
{user_question}
"""

FUNCTION_CALLING_PROMPT_TEMPLATE = """
In this environment you have access to a set of tools you can use
to answer the user's question. You may call them like this. 
Only invoke one signal tool at a time and wait for the results before
invoking another tool:
<function_calls>
<invoke>
<tool_name>$TOOL_NAME</tool_name>
<parameters>
<$PARAMETER_NAME>$PARAMETER_VALUE</PARAMETER_NAME>
...
</parameters>
</invoke>
</function_calls>

Here are the tools available:
<tools>
{tools_string}
</tools>
"""
