# api/gemini_client.py

import google.generativeai as genai
import os

class GeminiClient:
    """Client for Google's Gemini API."""
    
    def __init__(self, api_key=None):
        """Initialize the Gemini API client."""
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key is required")
            
        # Configure the Gemini API
        genai.configure(api_key=self.api_key)
    
    def generate_text(self, system_prompt, user_input, model="gemini-pro", 
                      temperature=0.7, max_tokens=4000):
        """Generate text using the Gemini API."""
        try:
            # Combine system prompt and user input for Gemini
            combined_prompt = f"{system_prompt}\n\nUser query: {user_input}"
            
            # Get the model
            model = genai.GenerativeModel(model)
            
            # Generate content
            response = model.generate_content(
                combined_prompt,
                generation_config=genai.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                    top_p=0.95,
                    top_k=40
                )
            )
            
            # Extract and return the text
            return response.text
            
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return f"Error in Gemini API call: {str(e)}"
