from anthropic import AnthropicVertex
import os
from dotenv import load_dotenv
from tools_schema import (
    set_reminder_schema,
    get_current_datetime_schema,
    add_duration_to_datetime_schema
)
from helpers import (
    add_user_message,
    run_conversation
)

load_dotenv()

google_vertex_project_id = os.getenv("PROJECT_ID")
model = os.getenv("MODEL")

client = AnthropicVertex(region="global", project_id=str(google_vertex_project_id))

messages = []
add_user_message(
    messages, 
    "Set a reminder for my doctors appointment.Its 177 days after Jan 1st, 2050."
)
run_conversation(client, model, messages, [
    get_current_datetime_schema,
    add_duration_to_datetime_schema,
    set_reminder_schema
])


    