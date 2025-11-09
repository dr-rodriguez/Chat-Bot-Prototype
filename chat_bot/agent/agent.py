"""Langchain agent core for Chat-Bot-Prototype."""

from typing import Optional, List
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

from chat_bot.config.settings import Settings
from chat_bot.providers.base import BaseProvider
from chat_bot.providers.ollama import OllamaProvider
from chat_bot.providers.gemini import GeminiProvider


class ChatAgent:
    """Langchain-based chat agent with multi-provider support."""
    
    def __init__(
        self,
        provider: str = "ollama",
        model: Optional[str] = None,
        settings: Optional[Settings] = None,
        tools: Optional[List] = None,
    ):
        """Initialize chat agent.
        
        Args:
            provider: LLM provider name ("ollama" or "gemini")
            model: Optional model name override
            settings: Settings instance (creates new if not provided)
            tools: Optional list of Langchain tools for agent
        """
        self.settings = settings or Settings()
        self.provider_name = provider.lower()
        self.model = model
        self.tools = tools or []
        self.message_history: List = []
        
        # Initialize provider
        provider_config = self.settings.get_provider_config(self.provider_name)
        
        if self.provider_name == "ollama":
            self.provider: BaseProvider = OllamaProvider(provider_config, self.model)
        elif self.provider_name == "gemini":
            self.provider: BaseProvider = GeminiProvider(provider_config, self.model)
        else:
            raise ValueError(f"Unknown provider: {provider}")
        
        # Initialize agent if tools are provided
        self.agent_executor: Optional[AgentExecutor] = None
        if self.tools:
            self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize Langchain agent with tools."""
        llm = self.provider.get_llm()
        
        # Simple ReAct prompt template
        prompt = PromptTemplate.from_template(
            """You are a helpful AI assistant. Use the following tools to answer questions.

Tools: {tools}

Use the following format:

Question: the input question you must answer
Thought: you should think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""
        )
        
        agent = create_react_agent(llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=False,
        )
    
    def invoke(self, message: str) -> str:
        """Invoke the agent with a message.
        
        Args:
            message: User message text
            
        Returns:
            Agent response text
        """
        # Add to message history
        self.message_history.append(HumanMessage(content=message))
        
        # Use agent executor if tools are available, otherwise use provider directly
        if self.agent_executor:
            response = self.agent_executor.invoke({"input": message})
            response_text = response.get("output", str(response))
        else:
            # Simple direct invocation without tools
            response_text = self.provider.invoke(message)
        
        # Add response to history
        self.message_history.append(AIMessage(content=response_text))
        
        return response_text
    
    def add_tool(self, tool):
        """Add a tool to the agent (requires reinitialization).
        
        Args:
            tool: Langchain tool instance
        """
        self.tools.append(tool)
        if self.tools:
            self._initialize_agent()
    
    def clear_history(self):
        """Clear message history."""
        self.message_history = []

