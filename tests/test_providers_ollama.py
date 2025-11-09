"""Unit tests for OllamaProvider class.

Mocking Strategy:
- urllib.request.urlopen is mocked to prevent actual HTTP requests to Ollama API
- langchain_ollama.OllamaLLM is mocked to prevent actual LLM initialization
- All network calls are intercepted and return predictable mock responses
"""

import json
from unittest.mock import MagicMock, patch
from urllib.error import URLError

import pytest

from chat_bot.providers.ollama import OllamaProvider


def test_ollama_provider_initialization():
    """Test that OllamaProvider initializes with config.
    
    Verifies that OllamaProvider can be instantiated with a valid
    configuration dictionary containing base_url and model.
    """
    config = {"base_url": "http://localhost:11434", "model": "llama3.2"}
    provider = OllamaProvider(config)
    
    assert provider.base_url == "http://localhost:11434"
    assert provider.model == "llama3.2"
    assert provider.config == config


@patch("chat_bot.providers.ollama.urlopen")
def test_ollama_get_available_models(mock_urlopen):
    """Test that _get_available_models() returns model list with mocked urlopen.
    
    Verifies that _get_available_models() correctly fetches and parses
    the list of available models from the Ollama API endpoint, using
    mocked HTTP responses.
    """
    # Setup mock response
    mock_response = MagicMock()
    mock_response.read.return_value.decode.return_value = json.dumps({
        "models": [
            {"name": "llama3.2:3b"},
            {"name": "llama3.2:1b"},
            {"name": "gemma2:2b"}
        ]
    })
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    config = {"base_url": "http://localhost:11434", "model": "llama3.2"}
    provider = OllamaProvider(config)
    
    models = provider._get_available_models()
    
    assert len(models) == 3
    assert "llama3.2:3b" in models
    assert "llama3.2:1b" in models
    assert "gemma2:2b" in models


@patch("chat_bot.providers.ollama.urlopen")
def test_ollama_get_available_models_network_error(mock_urlopen):
    """Test that network errors are handled gracefully.
    
    Verifies that _get_available_models() handles network errors
    gracefully by returning an empty list instead of raising exceptions.
    """
    # Setup mock to raise URLError
    mock_urlopen.side_effect = URLError("Connection refused")
    
    config = {"base_url": "http://localhost:11434", "model": "llama3.2"}
    provider = OllamaProvider(config)
    
    models = provider._get_available_models()
    
    # Should return empty list on error
    assert models == []


@patch("chat_bot.providers.ollama.urlopen")
def test_ollama_match_model_exact(mock_urlopen):
    """Test that exact model matching works.
    
    Verifies that _match_model() correctly matches a model name that
    exactly matches one of the available models.
    """
    # Setup mock response
    mock_response = MagicMock()
    mock_response.read.return_value.decode.return_value = json.dumps({
        "models": [
            {"name": "llama3.2:3b"},
            {"name": "llama3.2:1b"}
        ]
    })
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    config = {"base_url": "http://localhost:11434", "model": "llama3.2:3b"}
    provider = OllamaProvider(config)
    
    matched = provider._match_model("llama3.2:3b")
    
    assert matched == "llama3.2:3b"


@patch("chat_bot.providers.ollama.urlopen")
def test_ollama_match_model_prefix(mock_urlopen):
    """Test that prefix model matching works.
    
    Verifies that _match_model() correctly matches a model name using
    prefix matching when the requested model doesn't include a tag.
    """
    # Setup mock response
    mock_response = MagicMock()
    mock_response.read.return_value.decode.return_value = json.dumps({
        "models": [
            {"name": "llama3.2:3b"},
            {"name": "llama3.2:1b"}
        ]
    })
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    config = {"base_url": "http://localhost:11434", "model": "llama3.2"}
    provider = OllamaProvider(config)
    
    matched = provider._match_model("llama3.2")
    
    # Should match first model with prefix
    assert matched == "llama3.2:3b"


@patch("chat_bot.providers.ollama.urlopen")
def test_ollama_match_model_tagged(mock_urlopen):
    """Test that tagged model requires exact match.
    
    Verifies that _match_model() requires an exact match when the
    requested model includes a tag (contains ':').
    """
    # Setup mock response
    mock_response = MagicMock()
    mock_response.read.return_value.decode.return_value = json.dumps({
        "models": [
            {"name": "llama3.2:3b"},
            {"name": "llama3.2:1b"}
        ]
    })
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    config = {"base_url": "http://localhost:11434", "model": "llama3.2:3b"}
    provider = OllamaProvider(config)
    
    # Tagged model that doesn't exist should raise ValueError
    with pytest.raises(ValueError, match="not found"):
        provider._match_model("llama3.2:5b")


@patch("chat_bot.providers.ollama.urlopen")
def test_ollama_match_model_not_found(mock_urlopen):
    """Test that ValueError is raised when model not found.
    
    Verifies that _match_model() raises ValueError with a helpful
    error message when no matching model is found.
    """
    # Setup mock response
    mock_response = MagicMock()
    mock_response.read.return_value.decode.return_value = json.dumps({
        "models": [
            {"name": "llama3.2:3b"},
            {"name": "llama3.2:1b"}
        ]
    })
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    config = {"base_url": "http://localhost:11434", "model": "unknown"}
    provider = OllamaProvider(config)
    
    with pytest.raises(ValueError, match="No model matching"):
        provider._match_model("unknown")


@patch("chat_bot.providers.ollama.urlopen")
@patch("chat_bot.providers.ollama.OllamaLLM")
def test_ollama_get_llm(mock_ollama_llm, mock_urlopen):
    """Test that get_llm() returns OllamaLLM instance (mocked).
    
    Verifies that get_llm() creates and returns an OllamaLLM instance
    with the matched model name and base URL.
    """
    # Setup mock response for model matching
    mock_response = MagicMock()
    mock_response.read.return_value.decode.return_value = json.dumps({
        "models": [
            {"name": "llama3.2:3b"}
        ]
    })
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    # Setup mock LLM
    mock_llm_instance = MagicMock()
    mock_ollama_llm.return_value = mock_llm_instance
    
    config = {"base_url": "http://localhost:11434", "model": "llama3.2"}
    provider = OllamaProvider(config)
    
    llm = provider.get_llm()
    
    assert llm == mock_llm_instance
    mock_ollama_llm.assert_called_once_with(
        model="llama3.2:3b",
        base_url="http://localhost:11434"
    )


@patch("chat_bot.providers.ollama.urlopen")
@patch("chat_bot.providers.ollama.OllamaLLM")
def test_ollama_invoke(mock_ollama_llm, mock_urlopen):
    """Test that invoke() returns LLM response.
    
    Verifies that invoke() correctly calls the LLM and returns
    the response from the mocked LLM instance.
    """
    # Setup mock response for model matching
    mock_response = MagicMock()
    mock_response.read.return_value.decode.return_value = json.dumps({
        "models": [
            {"name": "llama3.2:3b"}
        ]
    })
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    # Setup mock LLM
    mock_llm_instance = MagicMock()
    mock_llm_instance.invoke.return_value = "Test response"
    mock_ollama_llm.return_value = mock_llm_instance
    
    config = {"base_url": "http://localhost:11434", "model": "llama3.2"}
    provider = OllamaProvider(config)
    
    response = provider.invoke("Test prompt")
    
    assert response == "Test response"
    mock_llm_instance.invoke.assert_called_once_with("Test prompt")


@patch("chat_bot.providers.ollama.urlopen")
def test_ollama_get_model_name(mock_urlopen):
    """Test that get_model_name() returns matched model.
    
    Verifies that get_model_name() returns the matched model name
    after model matching has occurred.
    """
    # Setup mock response
    mock_response = MagicMock()
    mock_response.read.return_value.decode.return_value = json.dumps({
        "models": [
            {"name": "llama3.2:3b"}
        ]
    })
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    config = {"base_url": "http://localhost:11434", "model": "llama3.2"}
    provider = OllamaProvider(config)
    
    # Trigger model matching by calling get_llm()
    with patch("chat_bot.providers.ollama.OllamaLLM"):
        provider.get_llm()
    
    model_name = provider.get_model_name()
    
    assert model_name == "llama3.2:3b"


def test_ollama_validate_config():
    """Test that validate_config() checks required fields.
    
    Verifies that validate_config() raises ValueError when required
    fields (model or base_url) are missing.
    """
    # Test with valid config
    config = {"base_url": "http://localhost:11434", "model": "llama3.2"}
    provider = OllamaProvider(config)
    assert provider.validate_config() is True
    
    # Test with missing model
    config_no_model = {"base_url": "http://localhost:11434"}
    provider_no_model = OllamaProvider(config_no_model)
    provider_no_model.model = None
    with pytest.raises(ValueError, match="model name is required"):
        provider_no_model.validate_config()
    
    # Test with missing base_url
    config_no_url = {"model": "llama3.2"}
    provider_no_url = OllamaProvider(config_no_url)
    provider_no_url.base_url = None
    with pytest.raises(ValueError, match="base URL is required"):
        provider_no_url.validate_config()

