from langchain.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field
from typing import List, Dict, Any
from ..models import Message, User
from .. import db
from datetime import datetime, timedelta, timezone

class MessageSummarizerInput(BaseModel):
    user_id: str = Field(description="The ID of the user whose messages to summarize")
    time_period: str = Field(description="Time period for summarization: 'day', 'week', 'month', or 'all'", default="week")
    include_private: bool = Field(description="Whether to include private messages in summary", default=False)

class MessageSummarizerTool(BaseTool):
    name: str = "message_summarizer"
    description: str = "Summarizes a user's messages over a specified time period. Useful for understanding user communication patterns and content themes."
    args_schema: BaseModel = MessageSummarizerInput
    
    def _run(self, user_id: str, time_period: str = "week", include_private: bool = False) -> str:
        """Summarize user messages over a specified time period."""
        try:
            # Calculate the time filter based on period
            now = datetime.now(timezone.utc)
            if time_period == "day":
                start_date = now - timedelta(days=1)
            elif time_period == "week":
                start_date = now - timedelta(weeks=1)
            elif time_period == "month":
                start_date = now - timedelta(days=30)
            else:  # "all"
                start_date = datetime.min
            
            # Build query
            query = Message.query.filter(Message.author_id == user_id)
            
            # Apply time filter
            if time_period != "all":
                query = query.filter(Message.created_at >= start_date)
            
            # Apply privacy filter
            if not include_private:
                query = query.filter(Message.is_private == False)
            
            # Get messages
            messages = query.order_by(Message.created_at.desc()).all()
            
            if not messages:
                return f"No messages found for user {user_id} in the specified time period."
            
            # Extract message content for summarization
            message_contents = [msg.content for msg in messages]
            total_messages = len(messages)
            
            # Create a summary of the messages
            summary = f"User {user_id} has {total_messages} messages in the {time_period} period.\n\n"
            summary += "Message content summary:\n"
            
            # Group messages by general themes (simple keyword-based approach)
            themes = {
                "questions": [],
                "statements": [],
                "personal": [],
                "technical": []
            }
            
            for content in message_contents:
                content_lower = content.lower()
                if any(word in content_lower for word in ["?", "what", "how", "why", "when", "where", "who"]):
                    themes["questions"].append(content[:100] + "..." if len(content) > 100 else content)
                elif any(word in content_lower for word in ["i", "me", "my", "myself", "personal"]):
                    themes["personal"].append(content[:100] + "..." if len(content) > 100 else content)
                elif any(word in content_lower for word in ["code", "program", "function", "api", "database", "server"]):
                    themes["technical"].append(content[:100] + "..." if len(content) > 100 else content)
                else:
                    themes["statements"].append(content[:100] + "..." if len(content) > 100 else content)
            
            # Add theme summaries
            for theme, messages_list in themes.items():
                if messages_list:
                    summary += f"\n{theme.title()} messages ({len(messages_list)}):\n"
                    for i, msg in enumerate(messages_list[:3]):  # Show first 3 examples
                        summary += f"  {i+1}. {msg}\n"
                    if len(messages_list) > 3:
                        summary += f"  ... and {len(messages_list) - 3} more\n"
            
            return summary
            
        except Exception as e:
            return f"Error summarizing messages: {str(e)}"
    
    async def _arun(self, user_id: str, time_period: str = "week", include_private: bool = False) -> str:
        """Async version of the tool."""
        return self._run(user_id, time_period, include_private) 