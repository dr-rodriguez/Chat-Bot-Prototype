"""Ollama provider implementation."""

from typing import Optional
from langchain_ollama import OllamaLLM

from chat_bot.providers.base import BaseProvider


class OllamaProvider(BaseProvider):
    """Ollama LLM provider implementation."""
    
    def __init__(self, config: dict, model: Optional[str] = "llama3.2"):
        """Initialize Ollama provider.
        
        Args:
            config: Configuration dict with 'base_url' and 'model'
            model: Optional model name override
        """
        super().__init__(config, model)
        self.base_url = config.get("base_url", "http://localhost:11434")
    
    def get_llm(self):
        """Get Ollama LLM instance."""
        if self._llm is None:
            self._llm = OllamaLLM(
                model=self.model,
                base_url=self.base_url,
            )
        return self._llm
    
    def invoke(self, prompt: str) -> str:
        """Invoke Ollama LLM with a prompt.
        
        Args:
            prompt: Input prompt text
            
        Returns:
            LLM response text
        """
        llm = self.get_llm()
        return llm.invoke(prompt)
    
    def validate_config(self) -> bool:
        """Validate Ollama configuration."""
        if not self.model:
            raise ValueError("Ollama model name is required")
        if not self.base_url:
            raise ValueError("Ollama base URL is required")
        return True

