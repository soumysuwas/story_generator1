# story_planner.py
from api.openai_client import OpenAIClient

class StoryPlanner:
    def __init__(self, api_client):
        self.api_client = api_client
        self.blueprint_prompt = """
        You are a master storyteller specialized in creating story blueprints.
        Based on the given concept, create a detailed story blueprint with:
        1. Overall story arc (beginning, middle, end)
        2. Major plot points (5-7 key events)
        3. Character profiles (3-5 main characters with traits, motivations, arcs)
        4. World building elements (setting, rules, important locations)
        This blueprint will be used to generate a multi-episode story.
        """
    
    def generate_blueprint(self, concept: str) -> str:
        """Generate a story blueprint based on concept"""
        return self.api_client.generate_text(
            system_prompt=self.blueprint_prompt,
            user_input=f"Create a story blueprint for: {concept}",
            temperature=0.8
        )
