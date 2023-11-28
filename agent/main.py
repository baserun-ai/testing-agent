#!/usr/bin/env python
import argparse
import logging
import os

from dotenv import load_dotenv
from langchain.agents import AgentType

import baserun
from agent.agent import run_agent

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)


def main():
    baserun.init()

    parser = argparse.ArgumentParser(description="An autonomous agent using Baserun")

    # Make user_input a positional argument
    parser.add_argument("user_input", help="User input for the agent.")
    parser.add_argument(
        "--provider",
        default="openai",
        choices=["openai", "anthropic"],
        help="Specify the provider.",
    )
    parser.add_argument("--use_streaming", action="store_true", help="Enable streaming.")

    # Use the actual enum values for choices
    parser.add_argument(
        "--agent_type",
        default=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION.value,
        choices=[e.value for e in AgentType],
        help="Type of the agent.",
    )

    args = parser.parse_args()

    username = os.getlogin()
    with baserun.with_session(username):
        run_agent(
            provider=args.provider,
            user_input=args.user_input,
            use_streaming=args.use_streaming,
            agent_type=args.agent_type,
        )


if __name__ == "__main__":
    main()
