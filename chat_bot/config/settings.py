"""Configuration management for Chat-Bot-Prototype."""

import os
from typing import Optional
from dotenv import load_dotenv


class Settings:
    """Application settings loaded from environment variables.

    This class manages configuration for different LLM providers by loading
    settings from environment variables or a .env file.

    Attributes
    ----------
    ollama_base_url : str
        Base URL for Ollama API.
    ollama_model : str
        Default Ollama model name.
    gemini_api_key : str, optional
        Google Gemini API key.
    gemini_model : str
        Default Gemini model name.
    model_memory_limit : int
        Maximum number of messages to keep in memory before trimming.
    mcp_url : str, optional
        URL of the MCP server endpoint for tool integration.

    """

    def __init__(self):
        """Load environment variables from .env file if present.

        Initializes all provider-specific settings from environment variables
        with default values where appropriate.

        """
        load_dotenv()

        # Ollama configuration
        self.ollama_base_url: str = os.getenv(
            "OLLAMA_BASE_URL", "http://localhost:11434"
        )
        self.ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.2")

        # Google Gemini configuration
        self.gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
        self.gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

        # Memory configuration
        self.model_memory_limit: int = int(
            os.getenv("MODEL_MEMORY_LIMIT", "20")
        )

        # MCP configuration
        mcp_url = os.getenv("MCP_URL")
        if mcp_url:
            mcp_url = mcp_url.strip()
            if not mcp_url:
                mcp_url = None
        self.mcp_url: Optional[str] = mcp_url

    def validate(self) -> bool:
        """Validate that required settings are present.

        Returns
        -------
        bool
            True if basic validation passes.

        """
        # Ollama doesn't require API keys, so it's always valid if base URL is set
        # Gemini requires API key
        return True  # Basic validation - can be extended

    def get_provider_config(self, provider: str) -> dict:
        """Get configuration dictionary for a specific provider.

        Parameters
        ----------
        provider : str
            Provider name ("ollama" or "gemini").

        Returns
        -------
        dict
            Configuration dictionary for the provider.

        Raises
        ------
        ValueError
            If provider is unknown or required settings are missing.

        """
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
