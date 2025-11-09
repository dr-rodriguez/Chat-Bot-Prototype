"""Unit tests for GeminiProvider class.

Mocking Strategy:
- langchain_google_genai.ChatGoogleGenerativeAI is mocked to prevent actual API initialization
- LLM invoke() method is mocked to return predictable message objects
- All API calls are intercepted and return mock responses without making actual HTTP requests
"""

from unittest.mock import MagicMock, patch

import pytest

from chat_bot.providers.gemini import GeminiProvider


def test_gemini_provider_initialization():
    """Test that GeminiProvider initializes with config.
    
    Verifies that GeminiProvider can be instantiated with a valid
    configuration dictionary containing api_key and model.
    """
    config = {"api_key": "test-api-key", "model": "gemini-2.5-flash"}
    provider = GeminiProvider(config)
    
    assert provider.api_key == "test-api-key"
    assert provider.model == "gemini-2.5-flash"
    assert provider.config == config


@patch("chat_bot.providers.gemini.ChatGoogleGenerativeAI")
def test_gemini_get_llm(mock_chat_google_genai):
    """Test that get_llm() returns ChatGoogleGenerativeAI instance (mocked).
    
    Verifies that get_llm() creates and returns a ChatGoogleGenerativeAI
    instance with the correct model and API key.
    """
    # Setup mock LLM
    mock_llm_instance = MagicMock()
    mock_chat_google_genai.return_value = mock_llm_instance
    
    config = {"api_key": "test-api-key", "model": "gemini-2.5-flash"}
    provider = GeminiProvider(config)
    
    llm = provider.get_llm()
    
    assert llm == mock_llm_instance
    mock_chat_google_genai.assert_called_once_with(
        model="gemini-2.5-flash",
        google_api_key="test-api-key"
    )


def test_gemini_get_llm_missing_api_key():
    """Test that ValueError is raised when API key missing.
    
    Verifies that get_llm() raises ValueError with a helpful error
    message when the API key is not provided in the configuration.
    """
    config = {"model": "gemini-2.5-flash"}  # No api_key
    provider = GeminiProvider(config)
    provider.api_key = None
    
    with pytest.raises(ValueError, match="API key is required"):
        provider.get_llm()


@patch("chat_bot.providers.gemini.ChatGoogleGenerativeAI")
def test_gemini_invoke(mock_chat_google_genai):
    """Test that invoke() returns LLM response content.
    
    Verifies that invoke() correctly calls the LLM and extracts
    the content from the response message object.
    """
    # Setup mock LLM
    mock_llm_instance = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "Test response content"
    mock_llm_instance.invoke.return_value = mock_message
    mock_chat_google_genai.return_value = mock_llm_instance
    
    config = {"api_key": "test-api-key", "model": "gemini-2.5-flash"}
    provider = GeminiProvider(config)
    
    response = provider.invoke("Test prompt")
    
    assert response == "Test response content"
    mock_llm_instance.invoke.assert_called_once_with("Test prompt")


@patch("chat_bot.providers.gemini.ChatGoogleGenerativeAI")
def test_gemini_invoke_message_object(mock_chat_google_genai):
    """Test that invoke() handles message objects correctly.
    
    Verifies that invoke() correctly handles different message object
    formats, including objects with content attributes and string responses.
    """
    # Setup mock LLM
    mock_llm_instance = MagicMock()
    
    # Test with message object that has content attribute
    mock_message = MagicMock()
    mock_message.content = "Message with content"
    mock_llm_instance.invoke.return_value = mock_message
    mock_chat_google_genai.return_value = mock_llm_instance
    
    config = {"api_key": "test-api-key", "model": "gemini-2.5-flash"}
    provider = GeminiProvider(config)
    
    response = provider.invoke("Test prompt")
    
    assert response == "Message with content"
    
    # Test with message object without content (falls back to str())
    mock_message_no_content = MagicMock()
    del mock_message_no_content.content  # Remove content attribute
    mock_message_no_content.__str__ = MagicMock(return_value="String representation")
    mock_llm_instance.invoke.return_value = mock_message_no_content
    
    response2 = provider.invoke("Test prompt 2")
    
    assert response2 == "String representation"


def test_gemini_get_model_name():
    """Test that get_model_name() returns model name.
    
    Verifies that get_model_name() returns the model name from
    the configuration.
    """
    config = {"api_key": "test-api-key", "model": "gemini-2.5-flash"}
    provider = GeminiProvider(config)
    
    model_name = provider.get_model_name()
    
    assert model_name == "gemini-2.5-flash"


def test_gemini_validate_config():
    """Test that validate_config() checks required fields.
    
    Verifies that validate_config() raises ValueError when required
    fields (api_key or model) are missing.
    """
    # Test with valid config
    config = {"api_key": "test-api-key", "model": "gemini-2.5-flash"}
    provider = GeminiProvider(config)
    assert provider.validate_config() is True
    
    # Test with missing API key
    config_no_key = {"model": "gemini-2.5-flash"}
    provider_no_key = GeminiProvider(config_no_key)
    provider_no_key.api_key = None
    with pytest.raises(ValueError, match="API key is required"):
        provider_no_key.validate_config()
    
    # Test with missing model
    config_no_model = {"api_key": "test-api-key"}
    provider_no_model = GeminiProvider(config_no_model)
    provider_no_model.model = None
    with pytest.raises(ValueError, match="model name is required"):
        provider_no_model.validate_config()

