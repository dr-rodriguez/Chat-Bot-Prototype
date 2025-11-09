"""Ollama provider implementation."""

from typing import Optional
import json
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from langchain_ollama import OllamaLLM

from chat_bot.providers.base import BaseProvider


class OllamaProvider(BaseProvider):
    """Ollama LLM provider implementation.
    
    This provider connects to a local or remote Ollama instance to run
    language models.
    
    Attributes
    ----------
    base_url : str
        Base URL for the Ollama API.
    _matched_model : str, optional
        Matched model name from available models.
    
    """
    
    def __init__(self, config: dict, model: Optional[str] = "llama3.2"):
        """Initialize Ollama provider.
        
        Parameters
        ----------
        config : dict
            Configuration dict with 'base_url' and 'model'.
        model : str, optional
            Optional model name override. Default is "llama3.2".
        
        """
        super().__init__(config, model)
        self.base_url = config.get("base_url", "http://localhost:11434")
        self._matched_model = None
    
    def _get_available_models(self) -> list[str]:
        """Get list of available Ollama models.
        
        Returns
        -------
        list[str]
            List of model names available in Ollama.
        
        """
        try:
            url = f"{self.base_url}/api/tags"
            request = Request(url)
            with urlopen(request, timeout=5) as response:
                data = json.loads(response.read().decode())
                return [model["name"] for model in data.get("models", [])]
        except (URLError, HTTPError, json.JSONDecodeError, TimeoutError):
            # If we can't fetch models, return empty list
            # This allows the code to still work if Ollama is not running
            return []
    
    def _match_model(self, requested_model: str) -> str:
        """Match requested model name to available models.
        
        If the requested model includes a tag (e.g., "llama3.2:3b"), it will
        match exactly. If it doesn't include a tag (e.g., "llama3.2"), it will
        match any model with that base name (e.g., "llama3.2:3b", "llama3.2:1b").
        
        Parameters
        ----------
        requested_model : str
            The model name requested by the user.
        
        Returns
        -------
        str
            Matched model name from available models.
        
        Raises
        ------
        ValueError
            If no matching model is found.
        
        """
        available_models = self._get_available_models()
        
        # If no models available, return the requested model as-is
        # (will fail later if it doesn't exist, but allows graceful degradation)
        if not available_models:
            return requested_model
        
        # Exact match first
        if requested_model in available_models:
            return requested_model
        
        # If requested model has a tag (contains ':'), require exact match
        if ':' in requested_model:
            raise ValueError(
                f"Model '{requested_model}' not found. Available models: {', '.join(available_models)}"
            )
        
        # If no tag, try prefix matching
        # Match models that start with "requested_model:"
        prefix = f"{requested_model}:"
        matching_models = [m for m in available_models if m.startswith(prefix)]
        
        if not matching_models:
            raise ValueError(
                f"No model matching '{requested_model}' found. Available models: {', '.join(available_models)}"
            )
        
        # If multiple matches, return the first one (could be made configurable)
        return matching_models[0]
    
    def get_llm(self):
        """Get Ollama LLM instance.
        
        Returns
        -------
        object
            Ollama LLM instance from langchain_ollama.
        
        """
        if self._llm is None:
            # Match the model to available models
            if self._matched_model is None:
                self._matched_model = self._match_model(self.model)
            
            self._llm = OllamaLLM(
                model=self._matched_model,
                base_url=self.base_url,
            )
        return self._llm
    
    def invoke(self, prompt: str) -> str:
        """Invoke Ollama LLM with a prompt.
        
        Parameters
        ----------
        prompt : str
            Input prompt text.
        
        Returns
        -------
        str
            LLM response text.
        
        """
        llm = self.get_llm()
        return llm.invoke(prompt)
    
    def validate_config(self) -> bool:
        """Validate Ollama configuration.
        
        Returns
        -------
        bool
            True if configuration is valid.
        
        Raises
        ------
        ValueError
            If model name or base URL is missing.
        
        """
        if not self.model:
            raise ValueError("Ollama model name is required")
        if not self.base_url:
            raise ValueError("Ollama base URL is required")
        return True

