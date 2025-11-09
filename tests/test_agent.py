"""Unit tests for ChatAgent class."""

from unittest.mock import MagicMock, patch

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

