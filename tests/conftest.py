"""Shared pytest fixtures for Chat-Bot-Prototype tests."""

from unittest.mock import MagicMock

import pytest

from chat_bot.config.settings import Settings


@pytest.fixture
def mock_settings():
    """Fixture providing Settings instance with test configuration.
    
    Returns a Settings instance configured for testing with default
    test values that can be overridden in individual tests.
    
    Returns
    -------
    Settings
        Settings instance with test configuration.
    """
    settings = Settings()
    # Override with test defaults
    settings.ollama_base_url = "http://localhost:11434"
    settings.ollama_model = "llama3.2"
    settings.gemini_api_key = "test-api-key"
    settings.gemini_model = "gemini-2.5-flash"
    return settings


@pytest.fixture
def mock_ollama_llm():
    """Fixture providing mock Ollama LLM instance.
    
    Returns a MagicMock configured to behave like an Ollama LLM
    with an invoke() method that returns a mock response.
    
    Returns
    -------
    MagicMock
        Mock Ollama LLM instance.
    """
    llm = MagicMock()
    llm.invoke.return_value = "Mock Ollama response"
    llm.model = "llama3.2:3b"
    llm.base_url = "http://localhost:11434"
    return llm


@pytest.fixture
def mock_gemini_llm():
    """Fixture providing mock Gemini LLM instance.
    
    Returns a MagicMock configured to behave like a Gemini LLM
    with an invoke() method that returns a mock message object.
    
    Returns
    -------
    MagicMock
        Mock Gemini LLM instance.
    """
    llm = MagicMock()
    # Gemini returns message objects with content attribute
    mock_message = MagicMock()
    mock_message.content = "Mock Gemini response"
    llm.invoke.return_value = mock_message
    llm.model = "gemini-2.5-flash"
    return llm


@pytest.fixture
def mock_agent():
    """Fixture providing mock ChatAgent instance for CLI tests.
    
    Returns a MagicMock configured to behave like a ChatAgent
    with invoke() and get_model_name() methods.
    
    Returns
    -------
    MagicMock
        Mock ChatAgent instance.
    """
    agent = MagicMock()
    agent.invoke.return_value = "Mock agent response"
    agent.get_model_name.return_value = "llama3.2:3b"
    agent.provider_name = "ollama"
    agent.model = "llama3.2:3b"
    return agent

