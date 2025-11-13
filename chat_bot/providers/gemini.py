"""Google Gemini provider implementation."""

from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI

from chat_bot.providers.base import BaseProvider


class GeminiProvider(BaseProvider):
    """Google Gemini LLM provider implementation.

    This provider connects to Google's Gemini API to run language models.

    Attributes
    ----------
    api_key : str, optional
        Google Gemini API key.

    """

    def __init__(self, config: dict, model: Optional[str] = None):
        """Initialize Gemini provider.

        Parameters
        ----------
        config : dict
            Configuration dict with 'api_key' and 'model'.
        model : str, optional
            Optional model name override.

        """
        super().__init__(config, model)
        self.api_key = config.get("api_key")

    def get_llm(self):
        """Get Gemini LLM instance.

        Returns
        -------
        object
            Gemini LLM instance from langchain_google_genai.

        Raises
        ------
        ValueError
            If API key is missing.

        """
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
        response = llm.invoke(prompt)
        # ChatGoogleGenerativeAI returns a message object, extract content
        if hasattr(response, "content"):
            return response.content["text"]
        return str(response)

    def validate_config(self) -> bool:
        """Validate Gemini configuration.

        Returns
        -------
        bool
            True if configuration is valid.

        Raises
        ------
        ValueError
            If API key or model name is missing.

        """
        if not self.api_key:
            raise ValueError("Gemini API key is required")
        if not self.model:
            raise ValueError("Gemini model name is required")
        return True
