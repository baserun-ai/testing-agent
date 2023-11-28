# Baserun demos

This is a collection of applications that demonstrate how Baserun is used.

## Getting started

1. Clone this repo
2. `poetry install`
3. Create a .env file with at least two environment variables: `BASERUN_API_KEY` and `OPENAI_API_KEY`

## Autonomous Agent

In the `agent/` module there is a basic autonomous agent built using langchain. To execute, run `python agent/main.py`.

## Chatbot

In the `chatbot/` module there is a basic implementation of a customer service chatbot. To execute,
run `python chatbot/main.py`