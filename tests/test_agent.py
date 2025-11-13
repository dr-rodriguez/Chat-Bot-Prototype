"""Unit tests for ChatAgent class."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from chat_bot.agent.agent import ChatAgent


@patch("chat_bot.agent.agent.OllamaProvider")
@patch("chat_bot.agent.agent.create_agent")
def test_agent_initialization_ollama(mock_create_agent, mock_ollama_provider, mock_settings):
    """Test that ChatAgent initializes correctly with Ollama provider.
    
    Verifies that ChatAgent can be instantiated with the "ollama" provider
    and that it correctly initializes the OllamaProvider and agent.
    """
    # Setup mocks
    mock_provider_instance = MagicMock()
    mock_provider_instance.get_llm.return_value = MagicMock()
    mock_ollama_provider.return_value = mock_provider_instance
    mock_agent_instance = MagicMock()
    mock_create_agent.return_value = mock_agent_instance
    
    # Create agent
    agent = ChatAgent(provider="ollama", settings=mock_settings)
    
    # Verify initialization
    assert agent.provider_name == "ollama"
    assert agent.settings == mock_settings
    mock_ollama_provider.assert_called_once()
    mock_create_agent.assert_called_once()


@patch("chat_bot.agent.agent.GeminiProvider")
@patch("chat_bot.agent.agent.create_agent")
def test_agent_initialization_gemini(mock_create_agent, mock_gemini_provider, mock_settings):
    """Test that ChatAgent initializes correctly with Gemini provider.
    
    Verifies that ChatAgent can be instantiated with the "gemini" provider
    and that it correctly initializes the GeminiProvider and agent.
    """
    # Setup mocks
    mock_provider_instance = MagicMock()
    mock_provider_instance.get_llm.return_value = MagicMock()
    mock_gemini_provider.return_value = mock_provider_instance
    mock_agent_instance = MagicMock()
    mock_create_agent.return_value = mock_agent_instance
    
    # Create agent
    agent = ChatAgent(provider="gemini", settings=mock_settings)
    
    # Verify initialization
    assert agent.provider_name == "gemini"
    assert agent.settings == mock_settings
    mock_gemini_provider.assert_called_once()
    mock_create_agent.assert_called_once()


def test_agent_initialization_unknown_provider(mock_settings):
    """Test that ChatAgent raises ValueError for unknown provider.
    
    Verifies that attempting to create a ChatAgent with an unknown provider
    raises a ValueError with an appropriate error message.
    """
    with pytest.raises(ValueError, match="Unknown provider"):
        ChatAgent(provider="unknown", settings=mock_settings)


@patch("chat_bot.agent.agent.OllamaProvider")
@patch("chat_bot.agent.agent.create_agent")
def test_agent_invoke(mock_create_agent, mock_ollama_provider, mock_settings):
    """Test that agent.invoke() returns response from mocked LLM.
    
    Verifies that invoking the agent with a message returns the expected
    response from the mocked agent.
    """
    # Setup mocks
    mock_provider_instance = MagicMock()
    mock_provider_instance.get_llm.return_value = MagicMock()
    mock_ollama_provider.return_value = mock_provider_instance
    
    mock_agent_instance = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "Test response"
    mock_agent_instance.invoke.return_value = {"messages": [mock_message]}
    mock_create_agent.return_value = mock_agent_instance
    
    # Create agent and invoke
    agent = ChatAgent(provider="ollama", settings=mock_settings)
    response = agent.invoke("Test message")
    
    # Verify response
    assert response == "Test response"
    mock_agent_instance.invoke.assert_called_once()


@patch("chat_bot.agent.agent.OllamaProvider")
@patch("chat_bot.agent.agent.create_agent")
def test_agent_add_tool(mock_create_agent, mock_ollama_provider, mock_settings):
    """Test that tool addition triggers agent reinitialization.
    
    Verifies that adding a tool to the agent causes the agent to be
    reinitialized with the new tool list.
    """
    # Setup mocks
    mock_provider_instance = MagicMock()
    mock_provider_instance.get_llm.return_value = MagicMock()
    mock_ollama_provider.return_value = mock_provider_instance
    
    mock_agent_instance = MagicMock()
    mock_create_agent.return_value = mock_agent_instance
    
    # Create agent
    agent = ChatAgent(provider="ollama", settings=mock_settings)
    
    # Reset call count after initial creation
    mock_create_agent.reset_mock()
    
    # Add tool
    mock_tool = MagicMock()
    agent.add_tool(mock_tool)
    
    # Verify agent was reinitialized
    assert len(agent.tools) == 1
    assert agent.tools[0] == mock_tool
    mock_create_agent.assert_called_once()


@patch("chat_bot.agent.agent.OllamaProvider")
@patch("chat_bot.agent.agent.create_agent")
def test_agent_get_model_name(mock_create_agent, mock_ollama_provider, mock_settings):
    """Test that get_model_name() returns correct model name.
    
    Verifies that get_model_name() correctly returns the model name
    from the provider.
    """
    # Setup mocks
    mock_provider_instance = MagicMock()
    mock_provider_instance.get_llm.return_value = MagicMock()
    mock_provider_instance.get_model_name.return_value = "llama3.2:3b"
    mock_ollama_provider.return_value = mock_provider_instance
    
    mock_agent_instance = MagicMock()
    mock_create_agent.return_value = mock_agent_instance
    
    # Create agent and get model name
    agent = ChatAgent(provider="ollama", settings=mock_settings)
    model_name = agent.get_model_name()
    
    # Verify model name
    assert model_name == "llama3.2:3b"
    mock_provider_instance.get_model_name.assert_called_once()


@patch("chat_bot.agent.agent.OllamaProvider")
@patch("chat_bot.agent.agent.create_agent")
def test_agent_clear_history(mock_create_agent, mock_ollama_provider, mock_settings):
    """Test that clear_history() method exists (no-op implementation).
    
    Verifies that the clear_history() method exists and can be called
    without raising an exception. The method is currently a no-op.
    """
    # Setup mocks
    mock_provider_instance = MagicMock()
    mock_provider_instance.get_llm.return_value = MagicMock()
    mock_ollama_provider.return_value = mock_provider_instance
    
    mock_agent_instance = MagicMock()
    mock_create_agent.return_value = mock_agent_instance
    
    # Create agent and call clear_history
    agent = ChatAgent(provider="ollama", settings=mock_settings)
    
    # Should not raise an exception
    agent.clear_history()


@patch("chat_bot.agent.agent.OllamaProvider")
@patch("chat_bot.agent.agent.create_agent")
@patch("chat_bot.agent.agent.MultiServerMCPClient")
def test_agent_loads_mcp_tools_success(mock_mcp_client, mock_create_agent, mock_ollama_provider, mock_settings):
    """Test that ChatAgent successfully loads MCP tools when MCP_URL is configured.
    
    Verifies that when MCP_URL is set, the agent connects to the MCP server,
    loads tools, and makes them available to the agent.
    """
    # Setup mocks
    mock_provider_instance = MagicMock()
    mock_provider_instance.get_llm.return_value = MagicMock()
    mock_ollama_provider.return_value = mock_provider_instance
    
    mock_agent_instance = MagicMock()
    mock_create_agent.return_value = mock_agent_instance
    
    # Setup MCP client mock
    mock_client_instance = MagicMock()
    mock_tool1 = MagicMock()
    mock_tool1.name = "mcp_tool_1"
    mock_tool2 = MagicMock()
    mock_tool2.name = "mcp_tool_2"
    mock_get_tools = AsyncMock(return_value=[mock_tool1, mock_tool2])
    mock_client_instance.get_tools = mock_get_tools
    mock_mcp_client.return_value = mock_client_instance
    
    # Configure settings with MCP_URL
    mock_settings.mcp_url = "http://localhost:8000/mcp"
    
    # Create agent
    agent = ChatAgent(provider="ollama", settings=mock_settings)
    
    # Verify MCP client was created
    mock_mcp_client.assert_called_once()
    
    # Verify tools were loaded and merged
    assert len(agent.tools) == 2
    assert agent.tools[0].name == "mcp_tool_1"
    assert agent.tools[1].name == "mcp_tool_2"
    
    # Verify agent was initialized with tools
    mock_create_agent.assert_called_once()


@patch("chat_bot.agent.agent.OllamaProvider")
@patch("chat_bot.agent.agent.create_agent")
def test_agent_backward_compatibility_no_mcp_url(mock_create_agent, mock_ollama_provider, mock_settings):
    """Test that ChatAgent works normally when MCP_URL is not set (backward compatibility).
    
    Verifies that the agent initializes successfully without MCP tools when
    MCP_URL is not configured, maintaining backward compatibility.
    """
    # Setup mocks
    mock_provider_instance = MagicMock()
    mock_provider_instance.get_llm.return_value = MagicMock()
    mock_ollama_provider.return_value = mock_provider_instance
    
    mock_agent_instance = MagicMock()
    mock_create_agent.return_value = mock_agent_instance
    
    # Configure settings without MCP_URL
    mock_settings.mcp_url = None
    
    # Create agent
    agent = ChatAgent(provider="ollama", settings=mock_settings)
    
    # Verify agent initialized successfully
    assert agent.provider_name == "ollama"
    assert agent.settings == mock_settings
    assert agent.tools == []
    mock_create_agent.assert_called_once()


@patch("chat_bot.agent.agent.OllamaProvider")
@patch("chat_bot.agent.agent.create_agent")
@patch("chat_bot.agent.agent.MultiServerMCPClient")
def test_agent_mcp_connection_timeout(mock_mcp_client, mock_create_agent, mock_ollama_provider, mock_settings):
    """Test that ChatAgent handles MCP connection timeout gracefully.
    
    Verifies that when MCP connection times out, the agent initializes
    successfully without MCP tools and logs an error.
    """
    import asyncio
    
    # Setup mocks
    mock_provider_instance = MagicMock()
    mock_provider_instance.get_llm.return_value = MagicMock()
    mock_ollama_provider.return_value = mock_provider_instance
    
    mock_agent_instance = MagicMock()
    mock_create_agent.return_value = mock_agent_instance
    
    # Setup MCP client mock to raise TimeoutError
    mock_client_instance = MagicMock()
    async def slow_get_tools():
        await asyncio.sleep(10)  # Longer than 5 second timeout
        return []
    mock_client_instance.get_tools = slow_get_tools
    mock_mcp_client.return_value = mock_client_instance
    
    # Configure settings with MCP_URL
    mock_settings.mcp_url = "http://localhost:8000/mcp"
    
    # Create agent (should handle timeout gracefully)
    agent = ChatAgent(provider="ollama", settings=mock_settings)
    
    # Verify agent initialized successfully without MCP tools
    assert agent.provider_name == "ollama"
    assert agent.tools == []
    mock_create_agent.assert_called_once()


@patch("chat_bot.agent.agent.OllamaProvider")
@patch("chat_bot.agent.agent.create_agent")
@patch("chat_bot.agent.agent.MultiServerMCPClient")
def test_agent_mcp_connection_error(mock_mcp_client, mock_create_agent, mock_ollama_provider, mock_settings):
    """Test that ChatAgent handles MCP connection errors gracefully.
    
    Verifies that when MCP connection fails, the agent initializes
    successfully without MCP tools and logs an error.
    """
    # Setup mocks
    mock_provider_instance = MagicMock()
    mock_provider_instance.get_llm.return_value = MagicMock()
    mock_ollama_provider.return_value = mock_provider_instance
    
    mock_agent_instance = MagicMock()
    mock_create_agent.return_value = mock_agent_instance
    
    # Setup MCP client mock to raise ConnectionError
    mock_client_instance = MagicMock()
    mock_get_tools = AsyncMock(side_effect=ConnectionError("Connection refused"))
    mock_client_instance.get_tools = mock_get_tools
    mock_mcp_client.return_value = mock_client_instance
    
    # Configure settings with MCP_URL
    mock_settings.mcp_url = "http://localhost:8000/mcp"
    
    # Create agent (should handle connection error gracefully)
    agent = ChatAgent(provider="ollama", settings=mock_settings)
    
    # Verify agent initialized successfully without MCP tools
    assert agent.provider_name == "ollama"
    assert agent.tools == []
    mock_create_agent.assert_called_once()


@patch("chat_bot.agent.agent.OllamaProvider")
@patch("chat_bot.agent.agent.create_agent")
@patch("chat_bot.agent.agent.MultiServerMCPClient")
def test_agent_mcp_invalid_url(mock_mcp_client, mock_create_agent, mock_ollama_provider, mock_settings):
    """Test that ChatAgent handles invalid MCP_URL gracefully.
    
    Verifies that when MCP_URL is invalid, the agent initializes
    successfully without MCP tools and logs an error.
    """
    # Setup mocks
    mock_provider_instance = MagicMock()
    mock_provider_instance.get_llm.return_value = MagicMock()
    mock_ollama_provider.return_value = mock_provider_instance
    
    mock_agent_instance = MagicMock()
    mock_create_agent.return_value = mock_agent_instance
    
    # Setup MCP client mock to raise ValueError
    mock_client_instance = MagicMock()
    mock_get_tools = AsyncMock(side_effect=ValueError("Invalid URL"))
    mock_client_instance.get_tools = mock_get_tools
    mock_mcp_client.return_value = mock_client_instance
    
    # Configure settings with invalid MCP_URL
    mock_settings.mcp_url = "not-a-valid-url"
    
    # Create agent (should handle invalid URL gracefully)
    agent = ChatAgent(provider="ollama", settings=mock_settings)
    
    # Verify agent initialized successfully without MCP tools
    assert agent.provider_name == "ollama"
    assert agent.tools == []
    mock_create_agent.assert_called_once()


@patch("chat_bot.agent.agent.OllamaProvider")
@patch("chat_bot.agent.agent.create_agent")
@patch("chat_bot.agent.agent.MultiServerMCPClient")
def test_agent_loads_multiple_mcp_tools(mock_mcp_client, mock_create_agent, mock_ollama_provider, mock_settings):
    """Test that ChatAgent loads multiple tools from MCP server.
    
    Verifies that when MCP server provides multiple tools, all of them
    are loaded and made available to the agent.
    """
    # Setup mocks
    mock_provider_instance = MagicMock()
    mock_provider_instance.get_llm.return_value = MagicMock()
    mock_ollama_provider.return_value = mock_provider_instance
    
    mock_agent_instance = MagicMock()
    mock_create_agent.return_value = mock_agent_instance
    
    # Setup MCP client mock with multiple tools
    mock_client_instance = MagicMock()
    mock_tools = []
    for i in range(5):
        mock_tool = MagicMock()
        mock_tool.name = f"mcp_tool_{i}"
        mock_tools.append(mock_tool)
    
    mock_get_tools = AsyncMock(return_value=mock_tools)
    mock_client_instance.get_tools = mock_get_tools
    mock_mcp_client.return_value = mock_client_instance
    
    # Configure settings with MCP_URL
    mock_settings.mcp_url = "http://localhost:8000/mcp"
    
    # Create agent
    agent = ChatAgent(provider="ollama", settings=mock_settings)
    
    # Verify all tools were loaded
    assert len(agent.tools) == 5
    for i in range(5):
        assert agent.tools[i].name == f"mcp_tool_{i}"
    
    # Verify agent was initialized with tools
    mock_create_agent.assert_called_once()


@patch("chat_bot.agent.agent.OllamaProvider")
@patch("chat_bot.agent.agent.create_agent")
@patch("chat_bot.agent.agent.MultiServerMCPClient")
def test_agent_mcp_tool_precedence(mock_mcp_client, mock_create_agent, mock_ollama_provider, mock_settings):
    """Test that MCP tools take precedence over existing tools with same name.
    
    Verifies that when an MCP tool has the same name as an existing tool,
    the MCP tool replaces the existing tool.
    """
    from langchain.tools import Tool
    
    # Setup mocks
    mock_provider_instance = MagicMock()
    mock_provider_instance.get_llm.return_value = MagicMock()
    mock_ollama_provider.return_value = mock_provider_instance
    
    mock_agent_instance = MagicMock()
    mock_create_agent.return_value = mock_agent_instance
    
    # Setup MCP client mock
    mock_client_instance = MagicMock()
    mock_mcp_tool = MagicMock()
    mock_mcp_tool.name = "search"  # Same name as existing tool
    mock_get_tools = AsyncMock(return_value=[mock_mcp_tool])
    mock_client_instance.get_tools = mock_get_tools
    mock_mcp_client.return_value = mock_client_instance
    
    # Configure settings with MCP_URL
    mock_settings.mcp_url = "http://localhost:8000/mcp"
    
    # Create existing tool with same name
    existing_tool = Tool(
        name="search",
        func=lambda x: f"Searching: {x}",
        description="Search tool"
    )
    
    # Create agent with existing tool
    agent = ChatAgent(provider="ollama", settings=mock_settings, tools=[existing_tool])
    
    # Verify MCP tool replaced existing tool
    assert len(agent.tools) == 1
    assert agent.tools[0].name == "search"
    assert agent.tools[0] == mock_mcp_tool  # MCP tool is used
    
    # Verify agent was initialized with merged tools
    mock_create_agent.assert_called_once()

