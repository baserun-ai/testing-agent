#!/usr/bin/env python
import argparse
import logging

import baserun as baserun
from baserun import Baserun
from dotenv import load_dotenv
from langchain.agents import initialize_agent, load_tools, AgentType
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
def main(provider="openai", user_input="", use_streaming=False, agent_type=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION):
    if not user_input:
        print("What would you like me to do?")
        print("> ", end="")
        user_input = input()

    llm = choose_llm(provider, use_streaming)

    tools = load_tools(["serpapi", "llm-math", "wikipedia"], llm=llm)

    agent_executor = initialize_agent(tools, llm, agent=agent_type, verbose=True)

    result = agent_executor.run(user_input)
    print(result)
    Baserun.log(name=f"{provider} Stream={use_streaming}", payload={"input": user_input, "result": result})
    return result


if __name__ == "__main__":
    Baserun.init()

    parser = argparse.ArgumentParser(description="Your Program Description Here")

    # Make user_input a positional argument
    parser.add_argument("user_input", help="User input for the agent.")
    parser.add_argument("--provider", default="openai", choices=["openai", "anthropic"], help="Specify the provider.")
    parser.add_argument("--use_streaming", action="store_true", help="Enable streaming.")

    # Use the actual enum values for choices
    parser.add_argument(
        "--agent_type",
        default=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION.value,
        choices=[e.value for e in AgentType],
        help="Type of the agent.",
    )

    args = parser.parse_args()

    main(
        provider=args.provider,
        user_input=args.user_input,
        use_streaming=args.use_streaming,
        agent_type=args.agent_type,
    )
