# utils/token_counter.py

import tiktoken

class TokenCounter:
    """Utility class for counting tokens in text."""
    
    def __init__(self, model="gpt-4o-mini"):
        """Initialize the token counter for a specific model."""
        try:
            self.encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            # Default to cl100k_base encoding if model-specific one not found
            self.encoding = tiktoken.get_encoding("cl100k_base")
        
        # Approximate token limits for various models
        self.model_token_limits = {
            "gpt-3.5-turbo": 4096,
            "gpt-4": 8192,
            "gpt-4o": 128000,
            "gpt-4o-mini": 128000
        }
        
        self.current_model = model
    
    def count_tokens(self, text):
        """Count the number of tokens in the given text."""
        if not text:
            return 0
        return len(self.encoding.encode(text))
    
    def truncate_text_to_token_limit(self, text, max_tokens):
        """Truncate text to fit within max_tokens."""
        if not text:
            return ""
            
        encoded = self.encoding.encode(text)
        if len(encoded) <= max_tokens:
            return text
            
        truncated = self.encoding.decode(encoded[:max_tokens])
        return truncated
    
    def get_model_limit(self):
        """Get the token limit for the current model."""
        return self.model_token_limits.get(self.current_model, 4096)
