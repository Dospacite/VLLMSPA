from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain.tools import BaseTool
from typing import List, Dict, Any, Optional
import json
from .message_summarizer import MessageSummarizerTool
from .model_info_tool import ModelInfoTool

class LangchainAgentService:
    def __init__(self, model_name: str = "llama3.1:8b-instruct-q8_0"):
        """Initialize the Langchain agent with tools."""
        self.model_name = model_name
        self.llm = OllamaLLM(model=model_name, base_url="http://ollama:11434")
        self.tools = self._setup_tools()
        self.agent = self._setup_agent()
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)
    
    def _setup_tools(self) -> List[BaseTool]:
        """Setup available tools for the agent."""
        tools = [
            MessageSummarizerTool(),
            ModelInfoTool()
        ]
        return tools
    
    def _setup_agent(self):
        """Setup the agent with prompt template."""
        system = '''
        Respond to the human as helpfully and accurately as possible. You have access to the following tools:

        {tools}
        
        Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).

        Valid "action" values: "Final Answer" or {tool_names}

        Provide only ONE action per $JSON_BLOB, as shown:

        ```
        {{
        "action": $TOOL_NAME,
        "action_input": $INPUT
        }}
        ```

        Follow this format:

        Question: input question to answer
        Thought: consider previous and subsequent steps
        Action:
        ```
        $JSON_BLOB
        ```
        Observation: action result
        ... (repeat Thought/Action/Observation N times)
        Thought: I know what to respond
        Action:
        ```
        {{
        "action": "Final Answer",
        "action_input": "Final response to human"
        }}

        Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation'''

        human = '''{input}
        {agent_scratchpad}
        (reminder to respond in a JSON blob no matter what)'''

        prompt = ChatPromptTemplate.from_messages([
            ("system", system),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", human),
        ])
        
        return create_structured_chat_agent(self.llm, self.tools, prompt)
    
    def chat(self, message: str, chat_history: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Process a chat message using the Langchain agent.
        
        Args:
            message: The user's message
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