# api/memory_llm.py
from .openai_client import OpenAIClient
from .perplexity_client import PerplexityClient
import os

class MemoryLLM:
    """Specialized LLM for memory management and consistency checking"""
    
    def __init__(self, api_type="openai", api_key=None):
        """Initialize the Memory LLM with a specific API"""
        if api_type.lower() == "openai":
            self.api_client = OpenAIClient(api_key=api_key or os.getenv("OPENAI_API_KEY"))
            # Use a more efficient model for memory tasks
            self.model = "gpt-3.5-turbo"
        elif api_type.lower() == "perplexity":
            self.api_client = PerplexityClient(api_key=api_key or os.getenv("PERPLEXITY_API_KEY"))
            self.model = "sonar-small-chat"
        else:
            raise ValueError(f"Unsupported API type: {api_type}")
    
    def generate_text(self, system_prompt, user_input, temperature=0.3, max_tokens=2000):
        """Generate text with the Memory LLM - uses lower temperature for more consistent output"""
        return self.api_client.generate_text(
            system_prompt=system_prompt,
            user_input=user_input,
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens
        )
