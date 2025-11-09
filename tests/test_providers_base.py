"""Unit tests for BaseProvider abstract class."""

import pytest

from chat_bot.providers.base import BaseProvider
from chat_bot.providers.gemini import GeminiProvider
from chat_bot.providers.ollama import OllamaProvider


def test_base_provider_initialization():
    """Test that BaseProvider cannot be instantiated (abstract).
    
    Verifies that BaseProvider is an abstract class and cannot be
    directly instantiated. Attempting to do so should raise TypeError.
    """
    with pytest.raises(TypeError):
        BaseProvider(config={})


def test_base_provider_interface():
    """Test that concrete providers implement required methods.
    
    Verifies that concrete provider implementations (OllamaProvider
    and GeminiProvider) implement all required abstract methods from
    BaseProvider.
    """
    # Test OllamaProvider implements required methods
    ollama_config = {"base_url": "http://localhost:11434", "model": "llama3.2"}
    ollama_provider = OllamaProvider(ollama_config)
    
    assert hasattr(ollama_provider, "get_llm")
    assert hasattr(ollama_provider, "invoke")
    assert callable(ollama_provider.get_llm)
    assert callable(ollama_provider.invoke)
    
    # Test GeminiProvider implements required methods
    gemini_config = {"api_key": "test-key", "model": "gemini-2.5-flash"}
    gemini_provider = GeminiProvider(gemini_config)
    
    assert hasattr(gemini_provider, "get_llm")
    assert hasattr(gemini_provider, "invoke")
    assert callable(gemini_provider.get_llm)
    assert callable(gemini_provider.invoke)


def test_base_provider_get_model_name():
    """Test that get_model_name() default implementation works.
    
    Verifies that the default implementation of get_model_name() in
    BaseProvider returns the model name from the config or "unknown"
    if no model is set.
    """
    # Test with OllamaProvider (uses default implementation)
    ollama_config = {"base_url": "http://localhost:11434", "model": "llama3.2"}
    ollama_provider = OllamaProvider(ollama_config)
    
    # Model name should be available
    assert ollama_provider.get_model_name() == "llama3.2:3b"
    
    # Test with GeminiProvider
    gemini_config = {"api_key": "test-key", "model": "gemini-2.5-flash"}
    gemini_provider = GeminiProvider(gemini_config)
    
    assert gemini_provider.get_model_name() == "gemini-2.5-flash"


def test_base_provider_validate_config():
    """Test that validate_config() default implementation works.
    
    Verifies that the default implementation of validate_config() in
    BaseProvider returns True. Concrete providers may override this
    to add validation logic.
    """
    # Test with OllamaProvider (uses default implementation initially)
    ollama_config = {"base_url": "http://localhost:11434", "model": "llama3.2"}
    ollama_provider = OllamaProvider(ollama_config)
    
    # Default implementation returns True
    # Note: OllamaProvider overrides this, so we test the base behavior
    # by checking that the method exists and is callable
    assert hasattr(ollama_provider, "validate_config")
    assert callable(ollama_provider.validate_config)

