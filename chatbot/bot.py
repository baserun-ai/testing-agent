import json
from uuid import uuid4

from openai import OpenAI

import baserun
from chatbot.tools import call_tool, TOOLS_SCHEMA
from chatbot.utils import message_from_tool_call, persist_conversation

EXIT = "exit"
PROMPT = """As a customer service representative for Joyful, the online pet product retailer, your main goal is to 
provide a positive and informative chat experience for customers inquiring about our products or their orders. 
Maintain a tone that is both approachable and professional, expressing empathy and offering apologies when a customer 
is dissatisfied.

Use the resources at your disposal, such as our product catalog, order tracking system, and FAQs, along with your 
knowledge of our products, to assist the customer. If a query falls beyond your capabilities or requires human 
intervention, smoothly transition the conversation to a live representative by stating, "I'm going to connect you 
with a member of our team who can assist you further," and then activate the `escalate` tool."""


@baserun.trace
def run_chatbot():
    client = OpenAI()
    conversation = [{"role": "system", "content": PROMPT}]
    conversation_id = str(uuid4())

    print(f"Start your conversation. Type `{EXIT}` to end the conversation.\n> ", end="")
    user_input = input()
    conversation.append({"role": "user", "content": user_input})
    with baserun.start_trace() as trace:
        while user_input != EXIT:
            completion = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=conversation,
                tools=TOOLS_SCHEMA,
            )
            message = completion.choices[0].message
            tool_calls = message.tool_calls
            if tool_calls:
                for tool_call in tool_calls:
                    conversation.append(message_from_tool_call(tool_call))
                    print(f"-- Calling tool {tool_call.function.name}")
                    result = call_tool(tool_call, conversation_id)
                    print(f"-- Tool call result: {result}")
                    conversation.append({"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id})
            else:
                content = message.content
                conversation.append({"role": "assistant", "content": content})
                print(f"{content}\n> ", end="")
                user_input = input()
                conversation.append({"role": "user", "content": user_input})

            # Persist the conversation and annotate the completion with its file stats
            file_stats = persist_conversation(conversation, conversation_id)
            annotation = baserun.annotate(completion_id=completion.id)
            annotation.log("Conversation persistence", file_stats)
            annotation.submit()

        trace.result = json.dumps(conversation)

        print("How would you rate this conversation on a scale of 1 to 10?\n> ", end="")
        user_feedback = input()

        # Annotate the trace with user feedback
        annotation = baserun.annotate(trace=trace)
        annotation.log("Conversation ID", {"conversation_id": conversation_id})
        annotation.feedback("Chatbot conversation rating", score=int(user_feedback))
        annotation.submit()
