"""Langchain agent core for Chat-Bot-Prototype."""

import asyncio
import logging
from typing import Any, Optional

from langchain.agents import AgentState, create_agent
from langchain.agents.middleware import before_model
from langchain.messages import RemoveMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langgraph.runtime import Runtime

from chat_bot.config.settings import Settings
from chat_bot.providers.base import BaseProvider
from chat_bot.providers.gemini import GeminiProvider
from chat_bot.providers.ollama import OllamaProvider

logger = logging.getLogger(__name__)


def create_trim_messages_middleware(memory_limit: int):
    """Create a trim_messages middleware function with configurable memory limit.
    
    Parameters
    ----------
    memory_limit : int
        Maximum number of messages to keep before trimming.
    
    Returns
    -------
    function
        Middleware function for trimming messages.
    """
    @before_model
    def trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        """Keep only the last few messages to fit context window.
        See https://docs.langchain.com/oss/python/langchain/short-term-memory
        """
        messages = state["messages"]

        # Keep first message plus the last memory_limit messages
        if len(messages) <= memory_limit:
            return None  # No changes needed

        first_msg = messages[0]
        recent_messages = messages[-memory_limit:]
        new_messages = [first_msg] + recent_messages

        return {"messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES), *new_messages]}
    
    return trim_messages


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
        self._loop = None  # Event loop for async operations

        # Initialize provider
        provider_config = self.settings.get_provider_config(self.provider_name)

        if self.provider_name == "ollama":
            self.provider: BaseProvider = OllamaProvider(provider_config, self.model)
        elif self.provider_name == "gemini":
            self.provider: BaseProvider = GeminiProvider(provider_config, self.model)
        else:
            raise ValueError(f"Unknown provider: {provider}")

        # Load MCP tools if configured
        if self.settings.mcp_url:
            mcp_tools = self._load_mcp_tools()
            if mcp_tools:
                self._merge_mcp_tools(mcp_tools)

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

        # Create trim_messages middleware with configured memory limit
        trim_messages = create_trim_messages_middleware(self.settings.model_memory_limit)

        self.agent = create_agent(
            model=llm,
            tools=self.tools,
            system_prompt=prompt,
            middleware=[trim_messages],
            checkpointer=InMemorySaver(),
        )

    def _get_or_create_loop(self):
        """Get existing event loop or create a new one.
        
        Returns
        -------
        asyncio.AbstractEventLoop
            An active event loop.
        
        """
        if self._loop is None or self._loop.is_closed():
            try:
                # Try to get the current event loop (if we're in an async context)
                loop = asyncio.get_running_loop()
                # If we're here, we're in an async context, so we can't use run_until_complete
                # This shouldn't happen in our sync invoke() method, but handle it gracefully
                return None
            except RuntimeError:
                # No running loop, check if there's a loop set but not running
                try:
                    self._loop = asyncio.get_event_loop()
                    if self._loop.is_closed():
                        raise RuntimeError("Event loop is closed")
                except RuntimeError:
                    # No event loop exists or it's closed, create a new one
                    self._loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(self._loop)
        return self._loop

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
        # Invoke the agent asynchronously to support async MCP tools
        # Memory is managed by the checkpointer
        # Reuse event loop to avoid "Event loop is closed" errors
        loop = self._get_or_create_loop()
        
        # Run the coroutine in the existing loop
        if loop is None or loop.is_running():
            # If we're in an async context or loop is running, use asyncio.run() as fallback
            # This creates a new loop, but it's necessary in this case
            response = asyncio.run(
                self.agent.ainvoke(
                    {"messages": [{"role": "user", "content": message}]},
                    {"configurable": {"thread_id": "1"}},
                )
            )
        else:
            # Use the existing loop (reuse it to avoid closing/reopening)
            response = loop.run_until_complete(
                self.agent.ainvoke(
                    {"messages": [{"role": "user", "content": message}]},
                    {"configurable": {"thread_id": "1"}},
                )
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

    def close(self):
        """Close the event loop and clean up resources.
        
        Call this method when you're done with the agent to properly
        clean up the event loop. This is optional but recommended for
        long-running applications.
        
        """
        if self._loop is not None and not self._loop.is_closed():
            self._loop.close()
            self._loop = None

    def _load_mcp_tools(self) -> list:
        """Load tools from MCP server and convert to LangChain tool format.

        Returns
        -------
        list
            List of LangChain tool objects from MCP server, or empty list on error.

        """
        if not self.settings.mcp_url:
            return []

        try:
            # Create MCP client with streamable HTTP transport
            client = MultiServerMCPClient({
                "mcp_server": {
                    "transport": "streamable_http",
                    "url": self.settings.mcp_url
                }
            })

            # Fetch tools (async method called from sync context)
            # Reuse event loop to avoid "Event loop is closed" errors
            loop = self._get_or_create_loop()
            if loop is None or loop.is_running():
                # If we're in an async context or loop is running, use asyncio.run() as fallback
                mcp_tools = asyncio.run(
                    asyncio.wait_for(client.get_tools(), timeout=5.0)
                )
            else:
                # Use the existing loop (reuse it to avoid closing/reopening)
                mcp_tools = loop.run_until_complete(
                    asyncio.wait_for(client.get_tools(), timeout=5.0)
                )

            if not mcp_tools:
                logger.warning("MCP server provided no tools")
                return []

            return mcp_tools

        except asyncio.TimeoutError:
            logger.error("Failed to load MCP tools: timeout after 5 seconds")
            return []
        except ConnectionError as e:
            logger.error(f"Failed to load MCP tools: connection error - {e}")
            return []
        except ValueError as e:
            logger.error(f"Failed to load MCP tools: invalid URL - {e}")
            return []
        except Exception as e:
            logger.error(f"Failed to load MCP tools: {e}")
            return []

    def _merge_mcp_tools(self, mcp_tools: list):
        """Merge MCP tools with existing tools, with MCP tools taking precedence.

        Parameters
        ----------
        mcp_tools : list
            List of MCP tools to merge.

        """
        # Create a dictionary of existing tools by name for conflict detection
        existing_tool_names = {tool.name for tool in self.tools if hasattr(tool, 'name')}

        # Check for conflicts and log warnings
        for tool in mcp_tools:
            if hasattr(tool, 'name') and tool.name in existing_tool_names:
                logger.warning(
                    f"MCP tool '{tool.name}' conflicts with existing tool, MCP tool will be used"
                )

        # Remove conflicting existing tools
        self.tools = [
            tool for tool in self.tools
            if not (hasattr(tool, 'name') and any(
                mcp_tool.name == tool.name
                for mcp_tool in mcp_tools
                if hasattr(mcp_tool, 'name')
            ))
        ]

        # Add all MCP tools (they take precedence)
        self.tools.extend(mcp_tools)
