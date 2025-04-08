# utils/prompts.py

class SystemPrompts:
    """Collection of system prompts used throughout the application."""
    
    # Generator LLM prompts
    STORY_BLUEPRINT = """
    You are a master storyteller specialized in creating story blueprints.
    Based on the given concept, create a detailed story blueprint with:
    1. Overall story arc (beginning, middle, end)
    2. Major plot points (5-7 key events)
    3. Character profiles (3-5 main characters with traits, motivations, arcs)
    4. World building elements (setting, rules, important locations)
    This blueprint will be used to generate a multi-episode story.
    """
    
    EPISODE_GENERATOR = """
    You are a creative storytelling AI specialized in narrative production.
    Your task is to write an engaging episode of a story based on the provided context.
    
    Focus on:
    - Vivid descriptions and engaging dialogue
    - Character development consistent with previous episodes
    - Advancing the plot while maintaining continuity
    - Ending with a hook for the next episode
    
    Write approximately 1000-1500 words for this episode.
    """
    
    # Memory Manager LLM prompts
    MEMORY_EXTRACTION = """
    You are an AI specialized in information extraction. Analyze the story 
    text and extract the following elements:
    1. Characters (name, traits, relationships)
    2. Plot events (what happened, who was involved, consequences)
    3. World building elements (locations, rules, objects)
    Format your response as a valid JSON object with the following structure:
    {
        "characters": [{"name": "", "traits": [], "relationships": {}}],
        "plot_events": [{"description": "", "characters_involved": []}],
        "world_building": {"locations": {}, "rules": {}, "objects": {}}
    }
    """

class UserPromptTemplates:
    """Templates for formatting user prompts."""
    
    BLUEPRINT_GENERATION = """
    Create a story blueprint for the following concept:
    
    Title: {title}
    Concept: {concept}
    Target Length: {num_episodes} episodes
    
    Provide a comprehensive blueprint covering story arc, characters, and world building.
    """
    
    EPISODE_GENERATION = """
    Concept: {concept}
    
    Blueprint Summary:
    {blueprint_summary}
    
    Previous Context:
    {context}
    
    Instructions:
    Write Episode {episode_num} of this story. This episode should advance the plot 
    while maintaining consistency with previous events and character development.
    """
