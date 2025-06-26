from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from ..models import Message, User

class MessageSummarizerInput(BaseModel):
    username: str = Field(description="The username of the user whose messages to summarize")

class MessageSummarizerTool(BaseTool):
    name: str = "message_summarizer"
    description: str = "Summarizes a user's messages."
    args_schema: Type[BaseModel] = MessageSummarizerInput
    
    def _run(self, username: str) -> str:
        """Summarize user messages over a specified time period."""
        try:
            # First find the user by username
            user = User.query.filter(User.username == username).first()
            
            if not user:
                return f"No user found with username '{username}'."
            
            # Build query for messages by user
            query = Message.query.filter(Message.author_id == user.id)
            
            # Get messages
            messages = query.order_by(Message.created_at.desc()).all()
            
            if not messages:
                return f"No messages found for user '{username}'."
            
            # Extract message content for summarization
            message_contents = [msg.content for msg in messages]
            
            
            return "\n".join(message_contents)
            
        except Exception as e:
            return f"Error summarizing messages: {str(e)}"
    
    async def _arun(self, username: str) -> str:
        """Async version"""
        return self._run(username)