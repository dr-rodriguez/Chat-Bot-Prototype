"""Base provider interface for LLM providers."""

from abc import ABC, abstractmethod
from typing import Optional


class BaseProvider(ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(self, config: dict, model: Optional[str] = None):
        """Initialize provider with configuration.
        
        Args:
            config: Provider-specific configuration dictionary
            model: Optional model name override
        """
        self.config = config
        self.model = model or config.get("model")
        self._llm = None
    
    @abstractmethod
    def get_llm(self):
        """Get the Langchain LLM instance for this provider.
        
        Returns:
            Langchain LLM instance
        """
        pass
    
    @abstractmethod
    def invoke(self, prompt: str) -> str:
        """Invoke the LLM with a prompt.
        
        Args:
            prompt: Input prompt text
            
        Returns:
            LLM response text
        """
        pass
    
    def validate_config(self) -> bool:
        """Validate provider configuration.
        
        Returns:
            True if configuration is valid
        """
        return True

