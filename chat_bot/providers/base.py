"""Base provider interface for LLM providers."""

from abc import ABC, abstractmethod
from typing import Optional


class BaseProvider(ABC):
    """Abstract base class for LLM providers.
    
    This class defines the interface that all LLM provider implementations
    must follow.
    
    Attributes
    ----------
    config : dict
        Provider-specific configuration dictionary.
    model : str, optional
        Model name to use.
    _llm : object, optional
        Cached Langchain LLM instance.
    
    """
    
    def __init__(self, config: dict, model: Optional[str] = None):
        """Initialize provider with configuration.
        
        Parameters
        ----------
        config : dict
            Provider-specific configuration dictionary.
        model : str, optional
            Optional model name override.
        
        """
        self.config = config
        self.model = model or config.get("model")
        self._llm = None
    
    @abstractmethod
    def get_llm(self):
        """Get the Langchain LLM instance for this provider.
        
        Returns
        -------
        object
            Langchain LLM instance.
        
        """
        pass
    
    @abstractmethod
    def invoke(self, prompt: str) -> str:
        """Invoke the LLM with a prompt.
        
        Parameters
        ----------
        prompt : str
            Input prompt text.
        
        Returns
        -------
        str
            LLM response text.
        
        """
        pass
    
    def get_model_name(self) -> str:
        """Get the actual model name being used.
        
        Returns
        -------
        str
            The model name currently in use.
        
        """
        return self.model or "unknown"
    
    def validate_config(self) -> bool:
        """Validate provider configuration.
        
        Returns
        -------
        bool
            True if configuration is valid.
        
        """
        return True

