# narrative_engine.py
from api.openai_client import OpenAIClient
from memory.memory_manager import MemoryManager
from evaluation.consistency_checker import ConsistencyChecker



class NarrativeEngine:
    def __init__(self, api_client, memory_manager):
        self.api_client = api_client
        self.memory_manager = memory_manager
        self.consistency_checker = ConsistencyChecker(api_client)  # Initialize consistency checker
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
        """Generate a story episode with consistency checking and compressed context."""
        # Truncate the blueprint to save tokens
        blueprint_summary = blueprint[:500] + "..." if len(blueprint) > 500 else blueprint
        
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
        
        # Check for inconsistencies
        try:
            inconsistencies = self.consistency_checker.check_consistency(episode, context)
            
            # If inconsistencies are found, try to fix them
            if inconsistencies:
                print(f"Found {len(inconsistencies)} inconsistencies. Attempting to fix...")
                
                # Create a prompt to fix inconsistencies
                fix_prompt = f"""
                You are a creative storytelling AI specialized in narrative production.
                The episode you generated has the following inconsistencies:
                {inconsistencies}
                
                Please rewrite the episode to fix these issues while maintaining the same 
                overall plot and character development.
                """
                
                # Generate a fixed version
                fixed_episode = self.api_client.generate_text(
                    system_prompt=fix_prompt,
                    user_input=episode,
                    temperature=0.5,
                    max_tokens=4000
                )
                
                # Use the fixed version if it's not empty
                if fixed_episode:
                    episode = fixed_episode
        except Exception as e:
            print(f"Error during consistency checking: {e}")
            # Continue with the original episode if consistency checking fails

        
        # Update memory with the new episode content
        self.memory_manager.update_memory(episode, episode_num)
        
        return episode

