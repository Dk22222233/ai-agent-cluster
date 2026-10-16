"""
The boundary between app-level ORM rows and agent-level DTOs.

This is the ONLY module in app/ that imports both sides. Everything
else speaks one language. Translation is symmetric:
    orm_to_agent_messages    : MessageModel[]   → Message[]
    agent_message_to_orm_fields : AssistantMessage → dict (ORM columns)
"""