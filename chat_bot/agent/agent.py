"""Langchain agent core for Chat-Bot-Prototype."""

from typing import Optional, List
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage

from chat_bot.config.settings import Settings
from chat_bot.providers.base import BaseProvider
from chat_bot.providers.ollama import OllamaProvider
from chat_bot.providers.gemini import GeminiProvider


class ChatAgent:
    """Langchain-based chat agent with multi-provider support.
    
    This agent provides a unified interface for interacting with different
    LLM providers and can be extended with tools for more complex tasks.
    
    Attributes
    ----------
    settings : Settings
        Application settings instance.
    provider_name : str
        Name of the LLM provider being used.
    model : str, optional
        Model name override.
    tools : list
        List of Langchain tools available to the agent.
    message_history : list
        History of messages in the conversation.
    provider : BaseProvider
        The LLM provider instance.
    agent : object, optional
        Langchain agent instance (if tools are provided).
    
    """
    
    def __init__(
        self,
        provider: str = "ollama",
        model: Optional[str] = None,
        settings: Optional[Settings] = None,
        tools: Optional[List] = None,
    ):
        """Initialize chat agent.
        
        Parameters
        ----------
        provider : str, optional
            LLM provider name ("ollama" or "gemini"). Default is "ollama".
        model : str, optional
            Optional model name override.
        settings : Settings, optional
            Settings instance (creates new if not provided).
        tools : list, optional
            Optional list of Langchain tools for agent.
        
        Raises
        ------
        ValueError
            If provider name is unknown.
        
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
        self.agent = None
        if self.tools:
            self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize Langchain agent with tools.
        
        Creates a ReAct-style agent with the configured tools and LLM.
        
        """
        llm = self.provider.get_llm()
        
        # Simple prompt template
        prompt = "You are a helpful AI assistant. Use the available tools to answer questions when needed."
        
        self.agent = create_agent(model=llm, tools=self.tools, system_prompt=prompt)
    
    def invoke(self, message: str) -> str:
        """Invoke the agent with a message.
        
        Parameters
        ----------
        message : str
            User message text.
        
        Returns
        -------
        str
            Agent response text.
        
        """
        # Add to message history
        self.message_history.append(HumanMessage(content=message))
        
        # Use agent executor if tools are available, otherwise use provider directly
        if self.agent:
            response = self.agent.invoke({"input": message})
            response_text = response.get("output", str(response))
        else:
            # Simple direct invocation without tools
            response_text = self.provider.invoke(message)
        
        # Add response to history
        self.message_history.append(AIMessage(content=response_text))
        
        return response_text
    
    def add_tool(self, tool):
        """Add a tool to the agent (requires reinitialization).
        
        Parameters
        ----------
        tool : object
            Langchain tool instance.
        
        """
        self.tools.append(tool)
        if self.tools:
            self._initialize_agent()
    
    def get_model_name(self) -> str:
        """Get the actual model name being used by the provider.
        
        Returns
        -------
        str
            The actual model name currently in use.
        
        """
        return self.provider.get_model_name()
    
    def clear_history(self):
        """Clear message history.
        
        Resets the conversation history to an empty list.
        
        """
        self.message_history = []

