import json
import os
from typing import Any

from openai.types.chat import ChatCompletionMessageToolCall


def persist_conversation(conversation: list[dict[str, str]], conversation_id: str) -> os.stat_result:
    """Persist the conversation to a JSON file and return stats about the saved file"""
    conversation_serialized = json.dumps(conversation)
    filename = f"conversation-{conversation_id}.json"
    with open(filename, "w+") as f:
        f.write(conversation_serialized)

    stats = os.stat(filename)
    return {"size": stats.st_size, "mode": stats.st_mode}


def message_from_tool_call(tool_call: ChatCompletionMessageToolCall) -> dict[str, Any]:
    return {
        "role": "assistant",
        "content": "",
        "tool_calls": [
            {
                "id": tool_call.id,
                "type": "function",
                "function": {
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments,
                },
            }
        ],
    }
