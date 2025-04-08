# narrative_engine.py
from api.openai_client import OpenAIClient
from memory.memory_manager import MemoryManager

class NarrativeEngine:
    def __init__(self, api_client, memory_manager):
        self.api_client = api_client
        self.memory_manager = memory_manager
        self.generator_prompt = """
        You are a creative storytelling AI specialized in narrative production.
        Your task is to write an engaging episode of a story based on the provided context.
        
        Focus on:
        - Vivid descriptions and engaging dialogue
        - Character development consistent with previous episodes
        - Advancing the plot while maintaining continuity
        - Ending with a hook for the next episode
        
        Write approximately 1000-1500 words for this episode.
        """
    
    def generate_episode(self, concept: str, blueprint: str, context: str, 
                        episode_num: int) -> str:
        """Generate a story episode"""
        user_input = f"""
        Concept: {concept}
        
        Blueprint Summary:
        {blueprint[:500]}...
        
        Previous Context:
        {context}
        
        Instructions:
        Write Episode {episode_num} of this story. This episode should advance the plot 
        while maintaining consistency with previous events and character development.
        """
        
        episode = self.api_client.generate_text(
            system_prompt=self.generator_prompt,
            user_input=user_input,
            temperature=0.7,
            max_tokens=4000
        )
        
        # Update memory with the new episode content
        self.memory_manager.update_memory(episode, episode_num)
        
        return episode
