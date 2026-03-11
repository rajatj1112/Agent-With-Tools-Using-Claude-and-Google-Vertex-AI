# Agent-With-Tools-Using-Claude-and-Google-Vertex-AI

A simple agentic AI system built with Claude models deployed through Google Vertex AI. This project demonstrates how to create an intelligent agent with custom tools that can reason about user requests and execute actions.

## Overview

This project implements an AI agent that:
- Uses Claude (Anthropic's language model) through Google Vertex AI
- Supports custom tool integration for extended functionality
- Executes tools like reminders, datetime operations, and duration calculations
- Handles multi-turn conversations with tool use reasoning

The agent can understand natural language requests, determine which tools to use, and execute them appropriately.

### Built-in Tools

- **set_reminder**: Creates timed reminders with specified content and timestamp
- **get_current_datetime**: Retrieves the current date and time in a specified format
- **add_duration_to_datetime**: Adds a duration (days, weeks, months, etc.) to a given datetime

## Project Structure

```
├── main.py                 # Main entry point - initializes and runs the agent
├── helpers.py             # Helper functions for agent operations
├── tools.py               # Custom tool implementations
├── tools_schema.py        # Tool definitions and schemas for the agent
├── requirements.txt       # Python package dependencies
└── README.md              # This file
```

## Prerequisites

- Python 3.8+
- Google Cloud account with Vertex AI enabled
- Google Cloud SDK installed
- Active Google Cloud project

## Setup Instructions

### 1. Google Cloud Authentication

Before running the agent, authenticate with Google Cloud:

```bash
gcloud init
```

This command will:
- Prompt you to log in with your Google account
- Set your default project
- Configure authentication credentials for local development

**Note:** When prompted, select the Google Cloud project you want to use for Vertex AI.

After initialization, set your project explicitly:

```bash
gcloud config set project YOUR_PROJECT_ID
```

### 2. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the project root directory with the following variables:

```
PROJECT_ID=your-google-cloud-project-id
MODEL=claude-3-5-sonnet@20241022
```

Replace `your-google-cloud-project-id` with your actual Google Cloud project ID.

## Usage

Run the agent:

```bash
python main.py
```

The agent will start with a default reminder message. You can modify the request in `main.py` by changing the message in the `add_user_message()` call.

### Example Usage

```python
# Set a custom message
add_user_message(
    messages, 
    "Set a reminder for my dentist appointment. It's 30 days from today."
)
run_conversation(client, model, messages, [
    get_current_datetime_schema,
    add_duration_to_datetime_schema,
    set_reminder_schema
])
```

## How It Works

1. **Message Processing**: User messages are added to the conversation history
2. **Agent Reasoning**: Claude analyzes the message and determines which tools to use
3. **Tool Execution**: The agent executes the selected tools with appropriate parameters
4. **Response Generation**: The agent generates a response based on tool outputs
5. **Conversation Loop**: The process repeats until the agent completes the task

## Troubleshooting

### Authentication Issues

If you encounter authentication errors:

1. Ensure you've run `gcloud init` and authenticated correctly
2. Verify your project ID is correct: `gcloud config get-value project`
3. Check that Vertex AI API is enabled in your Google Cloud project

### Missing Environment Variables

Ensure your `.env` file contains:
- `PROJECT_ID`: Your Google Cloud project ID
- `MODEL`: The Claude model name

### Tool Execution Errors

Check that tool inputs match the expected format in `tools_schema.py`

## Dependencies

- **anthropic**: Client library for Anthropic Vertex AI integration
- **python-dotenv**: Load environment variables from .env file

## License

This project is open source and available under the MIT License.
