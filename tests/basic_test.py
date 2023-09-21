from baserun import Baserun

from demo.main import main


def test_openai_non_streaming():
    Baserun.init()
    result = main(user_input="who won the 2022 nobel price in physics", provider="openai", use_streaming=False)
    assert "Zeilinger" in result


def test_openai_streaming():
    Baserun.init()
    result = main(user_input="who won the 2022 nobel price in physics", provider="openai", use_streaming=True)
    assert "Zeilinger" in result


def test_anthropic():
    Baserun.init()
    result = main(user_input="who won the 2022 nobel price in physics", provider="anthropic")
    assert "Zeilinger" in result
