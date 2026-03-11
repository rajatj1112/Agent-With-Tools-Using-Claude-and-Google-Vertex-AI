from anthropic.types import Message
import json
from tools import (
    set_reminder,
    get_current_datetime,
    add_duration_to_datetime
)


def add_user_message(messages, message):
    """
    Adds a user message to the conversation history.
    
    Args:
        messages (list): The conversation history list to append to.
        message (Message or str): The user message to add. Can be an Anthropic Message object
                                 or a string/dict.
    
    Returns:
        None: Modifies the messages list in-place.
    """
    user_message = {
        "role": "user",
        "content": message.content if isinstance(message, Message) else message
    }
    messages.append(user_message)
    
    
def add_assistant_message(messages, message):
    """
    Adds an assistant message to the conversation history.
    
    Args:
        messages (list): The conversation history list to append to.
        message (Message or str): The assistant message to add. Can be an Anthropic Message object
                                 or a string/dict.
    
    Returns:
        None: Modifies the messages list in-place.
    """
    assistant_message = {
        "role": "assistant",
        "content": message.content if isinstance(message, Message) else message
    }
    messages.append(assistant_message)


def chat(client, model, messages, system=None, temperature=1.0, stop_sequences=[], tools=None, tools_choice=None):
    """
    Sends a message to the Claude model via Vertex AI and retrieves a response.
    
    Args:
        client (AnthropicVertex): The Vertex AI client instance.
        model (str): The model identifier to use for the API call.
        messages (list): Conversation history with message objects containing roles and content.
        system (str, optional): System prompt to guide the model's behavior. Defaults to None.
        temperature (float, optional): Sampling temperature (0.0-2.0). Higher values increase randomness.
                                      Defaults to 1.0.
        stop_sequences (list, optional): List of sequences where the model should stop generating.
                                        Defaults to [].
        tools (list, optional): List of tool definitions available to the model. Defaults to None.
        tools_choice (str, optional): How the model should choose tools ('auto', 'any', 'tool').  Defaults to None.
    
    Returns:
        Message: The response message from Claude including content, stop_reason, and other metadata.
    """
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
    """
    Extracts all text content from a message and joins it with newlines.
    
    Args:
        message (Message): The message object containing content blocks.
    
    Returns:
        str: Concatenated text content with newlines between blocks.
    """
    return "\n".join(
        [block.text for block in message.content if block.type == "text"]
    )


def run_tool(tool_name, tool_inputs):
    """
    Executes a specific tool based on the tool name and provided inputs.
    
    Args:
        tool_name (str): The name of the tool to execute. Supported tools are:
                        'get_current_datetime', 'add_duration_to_datetime', 'set_reminder'.
        tool_inputs (dict): Dictionary of keyword arguments to pass to the tool function.
    
    Returns:
        Any: The output from the executed tool.
    
    Raises:
        If the tool_name doesn't match any supported tool, returns None implicitly.
    """
    if tool_name == "get_current_datetime":
        return get_current_datetime(**tool_inputs)
    elif tool_name == "add_duration_to_datetime":
        return add_duration_to_datetime(**tool_inputs)
    elif tool_name == "set_reminder":
        return set_reminder(**tool_inputs)


def run_tools(message):
    """
    Processes all tool use requests from a message and returns the results.
    
    Args:
        message (Message): The message object potentially containing tool use blocks.
    
    Returns:
        list: List of tool result blocks, each containing:
              - type: 'tool_result'
              - tool_result_id: The ID linking to the original tool request
              - content: JSON serialized output or error message
              - is_error: Boolean indicating if execution failed
    """
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
    """
    Runs a multi-turn conversation loop with tool use support.
    
    This function orchestrates the conversation flow:
    1. Sends a message to Claude with available tools
    2. Adds Claude's response to conversation history
    3. Extracts and executes any tool requests
    4. Adds tool results back to conversation
    5. Repeats until Claude stops requesting tools
    
    Args:
        client (AnthropicVertex): The Vertex AI client instance.
        model (str): The model identifier to use.
        messages (list): The conversation history list (modified in-place).
        tools_schemas (list): List of available tool schemas for the model.
    
    Returns:
        list: The complete conversation history after the loop completes.
    """
    while True:
        response = chat(client, model, messages, tools=tools_schemas)
        add_assistant_message(messages, response)
        print(text_from_message(response))
        
        if response.stop_reason != "tool_use":
            break
        
        tool_results = run_tools(response)
        add_user_message(messages, tool_results)
        
    return messages
