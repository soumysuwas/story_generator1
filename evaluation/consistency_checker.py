# evaluation/consistency_checker.py

import json
from api.openai_client import OpenAIClient
from utils.prompts import SystemPrompts

class ConsistencyChecker:
    """
    A class to check for narrative consistency across story episodes.
    """
    
    def __init__(self, api_client):
        """Initialize with an API client."""
        self.api_client = api_client
        self.consistency_prompt = """
        You are an AI specialized in narrative consistency analysis.
        Compare the new episode content against the established story elements.
        Identify any inconsistencies or contradictions with:
        1. Character traits, abilities, or motivations
        2. Previously established plot events or timelines
        3. World building rules or settings
        
        Format your response as a JSON object listing any inconsistencies found.
        If no inconsistencies are found, return an empty array.
        """
    
    def check_consistency(self, new_content, memory_context):
        """
        Check new story content against established memory for inconsistencies.
        """
        user_input = f"""
        Previous story context:
        {memory_context}
        
        New content to check:
        {new_content}
        
        Identify any inconsistencies between the new content and the established story elements.
        """
        
        response = self.api_client.generate_text(
            system_prompt=self.consistency_prompt,
            user_input=user_input,
            temperature=0.1  # Low temperature for more factual analysis
        )
        
        try:
            # Parse the response as JSON
            result = json.loads(response)
            return result if isinstance(result, list) else []
        except json.JSONDecodeError:
            # If response isn't valid JSON, try to extract inconsistencies manually
            inconsistencies = []
            if "inconsistenc" in response.lower():
                for line in response.split('\n'):
                    if ":" in line and any(x in line.lower() for x in ["character", "plot", "world"]):
                        inconsistencies.append(line.strip())
            return inconsistencies
    
    def get_consistency_score(self, inconsistencies):
        """Calculate a consistency score based on number of inconsistencies."""
        if not inconsistencies:
            return 1.0
        
        num_issues = len(inconsistencies)
        return max(0.0, 1.0 - (num_issues * 0.1))
