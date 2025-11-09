"""Configuration management for Chat-Bot-Prototype."""

import os
from typing import Optional
from dotenv import load_dotenv


class Settings:
    """Application settings loaded from environment variables."""
    
    def __init__(self):
        """Load environment variables from .env file if present."""
        load_dotenv()
        
        # Ollama configuration
        self.ollama_base_url: str = os.getenv(
            "OLLAMA_BASE_URL", 
            "http://localhost:11434"
        )
        self.ollama_model: str = os.getenv(
            "OLLAMA_MODEL",
            "llama3.2"
        )
        
        # Google Gemini configuration
        self.gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
        self.gemini_model: str = os.getenv(
            "GEMINI_MODEL",
            "gemini-flash"
        )
    
    def validate(self) -> bool:
        """Validate that required settings are present."""
        # Ollama doesn't require API keys, so it's always valid if base URL is set
        # Gemini requires API key
        return True  # Basic validation - can be extended
    
    def get_provider_config(self, provider: str) -> dict:
        """Get configuration dictionary for a specific provider."""
        if provider.lower() == "ollama":
            return {
                "base_url": self.ollama_base_url,
                "model": self.ollama_model,
            }
        elif provider.lower() == "gemini":
            if not self.gemini_api_key:
                raise ValueError(
                    "GEMINI_API_KEY environment variable is required for Gemini provider"
                )
            return {
                "api_key": self.gemini_api_key,
                "model": self.gemini_model,
            }
        else:
            raise ValueError(f"Unknown provider: {provider}")

