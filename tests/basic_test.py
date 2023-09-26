from datetime import datetime

import pytest
from baserun import Baserun
from langchain.agents import AgentType

from demo.main import main


@pytest.fixture
def user_input():
    return (
        f"Who won the 2022 Nobel Prize in Physics? It is the year {datetime.utcnow().year} and the award has "
        f"already been handed out."
    )


def test_openai_non_streaming(user_input):
    Baserun.init()
    result = main(user_input=user_input, provider="openai", use_streaming=False)
    assert "Zeilinger" in result
    Baserun.evals.includes("OpenAI Non-Streaming", result, ["Zeilinger"])


def test_openai_functions(user_input):
    Baserun.init()
    result = main(
        user_input=user_input, provider="openai", use_streaming=False, agent_type=AgentType.OPENAI_MULTI_FUNCTIONS
    )
    assert "Zeilinger" in result
    Baserun.evals.includes("OpenAI Non-Streaming", result, ["Zeilinger"])


def test_openai_streaming():
    Baserun.init()
    result = main(user_input=user_input, provider="openai", use_streaming=True)
    assert "Zeilinger" in result
    Baserun.evals.includes("OpenAI Streaming", result, ["Zeilinger"])


def test_anthropic():
    Baserun.init()
    result = main(user_input=user_input, provider="anthropic")
    assert "Zeilinger" in result
    Baserun.evals.includes("Anthropic", result, ["Zeilinger"])
