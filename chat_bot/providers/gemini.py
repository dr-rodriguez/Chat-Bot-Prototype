"""Google Gemini provider implementation."""

from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI

from chat_bot.providers.base import BaseProvider


class GeminiProvider(BaseProvider):
    """Google Gemini LLM provider implementation."""
    
    def __init__(self, config: dict, model: Optional[str] = None):
        """Initialize Gemini provider.
        
        Args:
            config: Configuration dict with 'api_key' and 'model'
            model: Optional model name override
        """
        super().__init__(config, model)
        self.api_key = config.get("api_key")
    
    def get_llm(self):
        """Get Gemini LLM instance."""
        if self._llm is None:
            if not self.api_key:
                raise ValueError("Gemini API key is required")
            self._llm = ChatGoogleGenerativeAI(
                model=self.model,
                google_api_key=self.api_key,
            )
        return self._llm
    
    def invoke(self, prompt: str) -> str:
        """Invoke Gemini LLM with a prompt.
        
        Args:
            prompt: Input prompt text
            
        Returns:
            LLM response text
        """
        llm = self.get_llm()
        response = llm.invoke(prompt)
        # ChatGoogleGenerativeAI returns a message object, extract content
        if hasattr(response, 'content'):
            return response.content
        return str(response)
    
    def validate_config(self) -> bool:
        """Validate Gemini configuration."""
        if not self.api_key:
            raise ValueError("Gemini API key is required")
        if not self.model:
            raise ValueError("Gemini model name is required")
        return True

