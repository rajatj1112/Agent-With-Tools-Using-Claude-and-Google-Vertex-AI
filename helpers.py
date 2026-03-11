from anthropic.types import Message
import json
from tools import (
    set_reminder,
    get_current_datetime,
    add_duration_to_datetime
)


def add_user_message(messages, message):
    user_message = {
        "role": "user",
        "content": message.content if isinstance(message, Message) else message
    }
    messages.append(user_message)
    
    
def add_assistant_message(messages, message):
    assistant_message = {
        "role": "assistant",
        "content": message.content if isinstance(message, Message) else message
    }
    messages.append(assistant_message)


def chat(client, model, messages, system=None, temperature=1.0, stop_sequences=[], tools=None, tools_choice=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences
    }
    
    if system:
        params["system"] = system
        
    if tools_choice:
        params["tools_choice"] = tools_choice
        
    if tools:
        params["tools"] = tools
        
    response = client.messages.create(**params)
    
    return response


def text_from_message(message):
    return "\n".join(
        [block.text for block in message.content if block.type == "text"]
    )


def run_tool(tool_name, tool_inputs):
    if tool_name == "get_current_datetime":
        return get_current_datetime(**tool_inputs)
    elif tool_name == "add_duration_to_datetime":
        return add_duration_to_datetime(**tool_inputs)
    elif tool_name == "set_reminder":
        return set_reminder(**tool_inputs)


def run_tools(message):
    # ToolUse Blocks
    tool_requests = [
        block for block in message.content if block.type == "tool_use"
    ]
    tool_results_blocks = []
    
    for tool_request in tool_requests:
        try:
            tool_output = run_tool(tool_request.name, tool_request.input)
            tool_result_block = {
                "type": "tool_result",
                "tool_result_id": tool_request.id,
                "content": json.dumps(tool_output),
                "is_error": False
            }
        except Exception as e:
            tool_result_block = {
                "type": "tool_result",
                "tool_result_id": tool_request.id,
                "content": f"Error: {e}",
                "is_error": True
            }
            
        tool_results_blocks.append(tool_result_block)
           
    return tool_results_blocks


def run_conversation(client, model, messages, tools_schemas):
    while True:
        response = chat(client, model, messages, tools=tools_schemas)
        add_assistant_message(messages, response)
        print(text_from_message(response))
        
        if response.stop_reason != "tool_use":
            break
        
        tool_results = run_tools(response)
        add_user_message(messages, tool_results)
        
    return messages
