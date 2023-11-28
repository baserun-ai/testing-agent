import json
from datetime import date
from typing import Any

from openai.types.chat import ChatCompletionMessageToolCall

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_products",
            "description": "Get product information including prices and stock counts",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "order_lookup",
            "description": "Looks up an order and shipping information",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "description": "The user's email address"},
                },
                "required": ["text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "escalate",
            "description": "Escalate this conversation to a human representative. Use if you are not likely to be "
            "able to fulfill the customer's request",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]

DOG_LEASH = {"name": "Tan Rope Dog Leash", "brand": "Reddy", "in_stock": 8, "price": 9.99}


def get_products() -> list[dict[str, Any]]:
    return [DOG_LEASH]


def order_lookup(email: str) -> list[dict[str, Any]]:
    # Ignore email, just return a predefined order for testing
    return [{"order_id": 1234, "items": [DOG_LEASH], "status": "shipped", "arrival_date": date.today().isoformat()}]


def escalate(conversation_id: str) -> bool:
    return True


def call_tool(tool_call: ChatCompletionMessageToolCall, conversation_id: str) -> Any:
    if tool_call.function.name == "get_products":
        return get_products()
    if tool_call.function.name == "order_lookup":
        return order_lookup(**json.loads(tool_call.function.arguments))

    return escalate(conversation_id)
