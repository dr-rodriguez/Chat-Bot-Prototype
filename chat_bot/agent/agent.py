"""Langchain agent core for Chat-Bot-Prototype."""

from typing import Any, Optional

from langchain.agents import AgentState, create_agent
from langchain.agents.middleware import before_model
from langchain.messages import RemoveMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langgraph.runtime import Runtime

from chat_bot.config.settings import Settings
from chat_bot.providers.base import BaseProvider
from chat_bot.providers.gemini import GeminiProvider
from chat_bot.providers.ollama import OllamaProvider


@before_model
def trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Keep only the last few messages to fit context window.
    See https://docs.langchain.com/oss/python/langchain/short-term-memory
    """
    messages = state["messages"]

    # Keep only the last 10 messages
    if len(messages) <= 10:
        return None  # No changes needed

    first_msg = messages[0]
    recent_messages = messages[-3:] if len(messages) % 2 == 0 else messages[-4:]
    new_messages = [first_msg] + recent_messages

    return {"messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES), *new_messages]}


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
        tools: Optional[list] = None,
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

        # Initialize provider
        provider_config = self.settings.get_provider_config(self.provider_name)

        if self.provider_name == "ollama":
            self.provider: BaseProvider = OllamaProvider(provider_config, self.model)
        elif self.provider_name == "gemini":
            self.provider: BaseProvider = GeminiProvider(provider_config, self.model)
        else:
            raise ValueError(f"Unknown provider: {provider}")

        # Initialize agent
        self.agent = None
        self._initialize_agent()

    def _initialize_agent(self):
        """Initialize Langchain agent with tools.

        Creates a ReAct-style agent with the configured tools and LLM.

        """
        llm = self.provider.get_llm()

        # Simple prompt template
        prompt = "You are a helpful AI assistant. Keep responses concise and to the point. Use the available tools to answer questions when needed."

        self.agent = create_agent(
            model=llm,
            tools=self.tools,
            system_prompt=prompt,
            middleware=[trim_messages],
            checkpointer=InMemorySaver(),
        )

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
        # Invoke the agent - memory is managed by the checkpointer
        response = self.agent.invoke(
            {"messages": [{"role": "user", "content": message}]},
            {"configurable": {"thread_id": "1"}},
        )

        # Extract the last AI message content from the response
        # The response contains a "messages" list with all conversation messages
        response_text = response["messages"][-1].content

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

        Note: This method currently does not clear the checkpointer's memory.
        To start a fresh conversation, use a different thread_id when invoking
        the agent, or create a new agent instance.

        """
        # Memory is managed by the checkpointer, not a local list
        # To clear history, use a different thread_id or create a new agent
        pass
