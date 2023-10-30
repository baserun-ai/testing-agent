import logging

from dotenv import load_dotenv
from langchain import LLMChain
from langchain.agents import load_tools, AgentType, initialize_agent
from langchain.schema import OutputParserException

import baserun
from baserun import Baserun
from baserun.templates import create_langchain_template
from demo.features import choose_llm

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

TEMPLATE = """
Answer the following questions as best you can. You have access to the following tools:

{tool_strings}

The way you use the tools is by specifying a json blob.
Specifically, this json should have a `action` key (with the name of the tool to use) and a `action_input` key (with the input to the tool going here).

The only values that should be in the "action" field are: {tool_names}

The $JSON_BLOB should only contain a SINGLE action, do NOT return a list of multiple actions. Here is an example of a valid $JSON_BLOB:

```
{{{{
  "action": $TOOL_NAME,
  "action_input": $INPUT
}}}}
```

ALWAYS use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action:
```
$JSON_BLOB
```
Observation: the result of the action
... (this Thought/Action/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question"

Begin! Reminder to always use the exact characters `Final Answer` when responding.

Question: {input}
"""


@baserun.trace
def run(provider="openai", user_input="", use_streaming=False, agent_type=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION):
    if not user_input:
        print("What would you like me to do?")
        print("> ", end="")
        user_input = input()

    llm = choose_llm(provider, use_streaming)
    tools = load_tools(["serpapi", "llm-math", "wikipedia"], llm=llm)
    tool_strings = "\n".join([f"{tool.name}: {tool.description}" for tool in tools])
    tool_names = ", ".join([tool.name for tool in tools])
    parameters = {"tool_names": tool_names, "tool_strings": tool_strings, "input": user_input}

    prompt = create_langchain_template(
        template_string=TEMPLATE,
        parameters=parameters,
        tools=tools,
        template_name="main_agent_prompt",
        template_tag="base",
    )

    llm_chain = LLMChain(llm=llm, prompt=prompt)

    agent_executor = initialize_agent(llm_chain=llm_chain, tools=tools, llm=llm, agent=agent_type, verbose=True)

    try:
        result = agent_executor.run(**parameters)
    except OutputParserException:
        parameters["input"] += ". Please remember to format your response correctly."
        result = agent_executor.run(**parameters)

    Baserun.log(name=f"{provider} Stream={use_streaming}", payload={"input": user_input, "result": result})

    return result
