from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain.tools import BaseTool
from typing import List, Dict, Any, Optional
import json
from .message_summarizer import MessageSummarizerTool

class LangchainAgentService:
    def __init__(self, model_name: str = "llama3.1:8b"):
        """Initialize the Langchain agent with tools."""
        self.model_name = model_name
        self.llm = OllamaLLM(model=model_name, base_url="http://ollama:11434")
        self.tools = self._setup_tools()
        self.agent = self._setup_agent()
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)
    
    def _setup_tools(self) -> List[BaseTool]:
        """Setup available tools for the agent."""
        tools = [
            MessageSummarizerTool()
        ]
        return tools
    
    def _setup_agent(self):
        """Setup the agent with prompt template."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful AI assistant with access to tools that can help you provide better responses.

Available tools:
- message_summarizer: Can summarize a user's messages over different time periods to understand their communication patterns and content themes.

When a user asks about their message history, communication patterns, or wants to understand their past interactions, use the message_summarizer tool to provide insights.

Always be helpful, friendly, and provide detailed responses. If you need to use a tool, explain why you're using it and what information you're gathering."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        return create_openai_tools_agent(self.llm, self.tools, prompt)
    
    def chat(self, message: str, user_id: Optional[str] = None, chat_history: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Process a chat message using the Langchain agent.
        
        Args:
            message: The user's message
            user_id: The user's ID (for tools that need it)
            chat_history: Previous chat messages
            
        Returns:
            Dict containing the response and any additional information
        """
        try:
            # Convert chat history to Langchain message format
            langchain_messages = []
            if chat_history:
                for msg in chat_history:
                    if msg.get('role') == 'user':
                        langchain_messages.append(HumanMessage(content=msg.get('content', '')))
                    elif msg.get('role') == 'assistant':
                        langchain_messages.append(AIMessage(content=msg.get('content', '')))
            
            # Add context about the user if available
            if user_id:
                context_message = f"Note: The current user's ID is {user_id}. You can use this ID with tools that need to access user-specific data."
                message = f"{context_message}\n\nUser message: {message}"
            
            # Execute the agent
            result = self.agent_executor.invoke({
                "input": message,
                "chat_history": langchain_messages
            })
            
            return {
                "response": result.get("output", ""),
                "model": self.model_name,
                "tools_used": result.get("intermediate_steps", []),
                "success": True
            }
            
        except Exception as e:
            return {
                "response": f"I encountered an error while processing your request: {str(e)}",
                "model": self.model_name,
                "tools_used": [],
                "success": False,
                "error": str(e)
            }
    
    def get_available_tools(self) -> List[Dict[str, str]]:
        """Get information about available tools."""
        return [
            {
                "name": tool.name,
                "description": tool.description
            }
            for tool in self.tools
        ] 