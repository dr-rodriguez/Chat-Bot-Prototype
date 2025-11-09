"""Unit tests for Settings class."""

from unittest.mock import patch

import pytest

from chat_bot.config.settings import Settings


def test_settings_initialization_defaults():
    """Test that Settings loads with default values.
    
    Verifies that Settings can be instantiated and loads default
    values when environment variables are not set.
    """
    def getenv_side_effect(key, default=None):
        # Return None for all keys to simulate env vars not being set
        # This allows the default parameter to be used
        return default
    
    with patch("chat_bot.config.settings.load_dotenv"):
        with patch("chat_bot.config.settings.os.getenv", side_effect=getenv_side_effect):
            settings = Settings()
            
            assert settings.ollama_base_url == "http://localhost:11434"
            assert settings.ollama_model == "llama3.2"
            assert settings.gemini_api_key is None
            assert settings.gemini_model == "gemini-2.5-flash"


@patch("chat_bot.config.settings.load_dotenv")
@patch("chat_bot.config.settings.os.getenv")
def test_settings_initialization_env_vars(mock_getenv, mock_load_dotenv):
    """Test that Settings loads from environment variables.
    
    Verifies that Settings correctly loads configuration values
    from environment variables when they are set.
    """
    # Setup mock to return different values for different env vars
    def getenv_side_effect(key, default=None):
        env_vars = {
            "OLLAMA_BASE_URL": "http://custom:11434",
            "OLLAMA_MODEL": "custom-model",
            "GEMINI_API_KEY": "custom-api-key",
            "GEMINI_MODEL": "custom-gemini-model"
        }
        return env_vars.get(key, default)
    
    mock_getenv.side_effect = getenv_side_effect
    
    settings = Settings()
    
    assert settings.ollama_base_url == "http://custom:11434"
    assert settings.ollama_model == "custom-model"
    assert settings.gemini_api_key == "custom-api-key"
    assert settings.gemini_model == "custom-gemini-model"


def test_settings_get_provider_config_ollama():
    """Test that Ollama config retrieval works.
    
    Verifies that get_provider_config() returns the correct
    configuration dictionary for the Ollama provider.
    """
    settings = Settings()
    settings.ollama_base_url = "http://localhost:11434"
    settings.ollama_model = "llama3.2"
    
    config = settings.get_provider_config("ollama")
    
    assert config == {
        "base_url": "http://localhost:11434",
        "model": "llama3.2"
    }


def test_settings_get_provider_config_gemini():
    """Test that Gemini config retrieval works.
    
    Verifies that get_provider_config() returns the correct
    configuration dictionary for the Gemini provider.
    """
    settings = Settings()
    settings.gemini_api_key = "test-api-key"
    settings.gemini_model = "gemini-2.5-flash"
    
    config = settings.get_provider_config("gemini")
    
    assert config == {
        "api_key": "test-api-key",
        "model": "gemini-2.5-flash"
    }


def test_settings_get_provider_config_gemini_missing_key():
    """Test that ValueError is raised when API key missing.
    
    Verifies that get_provider_config() raises ValueError with
    a helpful error message when the Gemini API key is not set.
    """
    settings = Settings()
    settings.gemini_api_key = None
    settings.gemini_model = "gemini-2.5-flash"
    
    with pytest.raises(ValueError, match="GEMINI_API_KEY"):
        settings.get_provider_config("gemini")


def test_settings_get_provider_config_unknown():
    """Test that ValueError is raised for unknown provider.
    
    Verifies that get_provider_config() raises ValueError with
    a helpful error message when an unknown provider is requested.
    """
    settings = Settings()
    
    with pytest.raises(ValueError, match="Unknown provider"):
        settings.get_provider_config("unknown")


def test_settings_validate():
    """Test that validate() returns True.
    
    Verifies that validate() returns True for valid settings.
    The current implementation always returns True, but this
    test ensures the method exists and works.
    """
    settings = Settings()
    
    assert settings.validate() is True

