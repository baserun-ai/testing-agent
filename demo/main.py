#!/usr/bin/env python
import logging
import sys

import baserun as baserun
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType, load_tools
from langchain.chat_models import ChatOpenAI

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)


@baserun.trace
def main(user_input=""):
    if not user_input:
        print("What would you like me to do?")
        print("> ", end="")
        user_input = input()

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k-0613")

    tools = load_tools(["serpapi", "llm-math", "wikipedia"], llm=llm)

    agent_executor = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    result = agent_executor.run(user_input)
    print(result)


if __name__ == "__main__":
    baserun.init()
    if sys.argv[-1] not in __file__:
        main(sys.argv[-1])
    else:
        main()
