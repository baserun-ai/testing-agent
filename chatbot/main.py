#!/usr/bin/env python
import os

from dotenv import load_dotenv

import baserun
from chatbot.bot import run_chatbot, PROMPT

load_dotenv()


def main():
    baserun.init()

    username = os.getlogin()
    baserun.register_template(template_string=PROMPT, template_name="Customer Service", template_tag="production")
    with baserun.with_session(username):
        run_chatbot()


if __name__ == "__main__":
    main()
