#!/usr/bin/env python
import logging
import sys

import baserun as baserun
from baserun import Baserun
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType, load_tools
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI, ChatAnthropic

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)


def choose_llm(provider: str, use_streaming: bool = False):
    if provider == "openai":
        if use_streaming:
            return ChatOpenAI(
                temperature=0,
                model_name="gpt-3.5-turbo-16k-0613",
                streaming=True,
                callbacks=[StreamingStdOutCallbackHandler()],
            )
        else:
            return ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k-0613")
    if provider == "anthropic":
        return ChatAnthropic(streaming=use_streaming)

    raise NotImplementedError


@baserun.trace
def main(provider="openai", user_input="", use_streaming=False):
    if not user_input:
        print("What would you like me to do?")
        print("> ", end="")
        user_input = input()

    llm = choose_llm(provider, use_streaming)

    tools = load_tools(["serpapi", "llm-math", "wikipedia"], llm=llm)

    agent_executor = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    result = agent_executor.run(user_input)
    print(result)
    return result


if __name__ == "__main__":
    Baserun.init()
    if sys.argv[-1] not in __file__:
        main(user_input=sys.argv[-1])
    else:
        main()
