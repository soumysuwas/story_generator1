# memory_manager.py
import json
from .schema import StoryMemory, Character, PlotEvent
from api.openai_client import OpenAIClient
from typing import Dict, List, Any
from .vector_store import VectorStore

class MemoryManager:
    def __init__(self, api_client):
        self.api_client = api_client
        self.memory = None
        self.vector_store = VectorStore()  # Initialize vector store
        self.extraction_prompt = """
        You are an AI specialized in information extraction. Analyze the story 
        text and extract the following elements:
        1. Characters (name, traits, relationships)
        2. Plot events (what happened, who was involved, consequences)
        3. World building elements (locations, rules, objects)

        Your response MUST be a valid JSON object with EXACTLY this structure:
        {
            "characters": [{"name": "Character Name", "traits": ["trait1", "trait2"], "relationships": {"other_character_name": "relationship_type"}}],
            "plot_events": [{"description": "Event description", "characters_involved": ["character1", "character2"]}],
            "world_building": {"locations": {"location_name": "description"}, "rules": {"rule_name": "description"}, "objects": {"object_name": "description"}}
        }

        IMPORTANT INSTRUCTIONS:
        1. Return ONLY the JSON object with no additional text before or after.
        2. Ensure all JSON keys and values are properly quoted with double quotes.
        3. Do not use single quotes, backticks, or any other delimiters for the JSON.
        4. Do not include any markdown formatting, explanations, or notes.
        5. Verify that your response is valid JSON before submitting.
        """
    
    def initialize_memory(self, concept: str, title: str) -> None:
        self.memory = StoryMemory(title=title, concept=concept)
    


    def extract_story_elements(self, story_text: str) -> Dict[str, Any]:
        """Extract story elements from generated text using LLM"""
        response = self.api_client.generate_text(
            system_prompt=self.extraction_prompt,
            user_input=f"Extract story elements from this text:\n{story_text}"
        )
        
        # Try multiple approaches to parse the JSON
        try:
            # First attempt: direct JSON parsing
            extracted = json.loads(response)
            return extracted
        except json.JSONDecodeError:
            print("Error parsing JSON from extraction response")
            
            # Second attempt: Try to extract JSON using regex
            import re
            json_match = re.search(r'(\{.*\})', response, re.DOTALL)
            if json_match:
                try:
                    json_str = json_match.group(1)
                    # Fix common JSON formatting issues
                    json_str = json_str.replace("'", '"')  # Replace single quotes with double quotes
                    json_str = re.sub(r'([{,])\s*(\w+):', r'\1"\2":', json_str)  # Add quotes to keys
                    extracted = json.loads(json_str)
                    return extracted
                except:
                    pass
            
            # Third attempt: Try to extract structured data even without proper JSON
            characters = []
            plot_events = []
            world_building = {"locations": {}, "rules": {}, "objects": {}}
            
            # Extract characters
            char_section = re.search(r'"characters"\s*:\s*\[(.*?)\]', response, re.DOTALL)
            if char_section:
                char_entries = re.findall(r'\{\s*"name"\s*:\s*"([^"]+)"', char_section.group(1))
                for name in char_entries:
                    characters.append({"name": name, "traits": [], "relationships": {}})
            
            # Extract plot events
            event_section = re.search(r'"plot_events"\s*:\s*\[(.*?)\]', response, re.DOTALL)
            if event_section:
                event_entries = re.findall(r'\{\s*"description"\s*:\s*"([^"]+)"', event_section.group(1))
                for desc in event_entries:
                    plot_events.append({"description": desc, "characters_involved": []})
            
            # Extract world building elements
            loc_section = re.search(r'"locations"\s*:\s*\{(.*?)\}', response, re.DOTALL)
            if loc_section:
                loc_entries = re.findall(r'"([^"]+)"\s*:\s*"([^"]+)"', loc_section.group(1))
                for name, desc in loc_entries:
                    world_building["locations"][name] = desc
            
            # If we extracted anything, return it
            if characters or plot_events or any(world_building.values()):
                return {
                    "characters": characters,
                    "plot_events": plot_events,
                    "world_building": world_building
                }
            
            # If all else fails, return a default structure
            return {
                "characters": [],
                "plot_events": [],
                "world_building": {"locations": {}, "rules": {}, "objects": {}}
            }


    
    def update_memory(self, story_text: str, episode: int) -> None:
        """Update memory with new story elements"""
        extracted = self.extract_story_elements(story_text)
        
        # Update characters
        for char in extracted.get("characters", []):
            char_id = char["name"].lower().replace(" ", "_")
            if char_id in self.memory.characters:
                # Update existing character
                existing_char = self.memory.characters[char_id]
                for trait in char.get("traits", []):
                    if trait not in existing_char.traits:
                        existing_char.traits.append(trait)
                for rel_id, rel_type in char.get("relationships", {}).items():
                    existing_char.relationships[rel_id] = rel_type
                existing_char.development.append({"episode": episode, "state": "Updated"})
            else:
                # Add new character
                self.memory.characters[char_id] = Character(
                    id=char_id,
                    name=char["name"],
                    traits=char.get("traits", []),
                    relationships=char.get("relationships", {}),
                    development=[{"episode": episode, "state": "Introduced"}]
                )
        
        # Update plot events
        for event in extracted.get("plot_events", []):
            event_id = f"e{episode}_{len(self.memory.plot_events)}"
            self.memory.plot_events.append(PlotEvent(
                id=event_id,
                episode=episode,
                scene=None,
                description=event["description"],
                characters_involved=event.get("characters_involved", [])
            ))
        
        # Update world building
        world = extracted.get("world_building", {})
        for loc_name, loc_details in world.get("locations", {}).items():
            self.memory.world_building.locations[loc_name] = loc_details
        for rule_name, rule_desc in world.get("rules", {}).items():
            self.memory.world_building.rules[rule_name] = rule_desc
        for obj_name, obj_details in world.get("objects", {}).items():
            self.memory.world_building.objects[obj_name] = obj_details
        
        # Update current episode
        self.memory.current_episode = episode
    
    def get_relevant_context(self, episode: int, max_tokens: int = 2000) -> str:
        """Retrieve relevant context for generating the next episode"""
        # TODO: Implement vector-based retrieval for more relevant context
        # For now, implement a simpler approach
        
        context = [f"Title: {self.memory.title}", f"Concept: {self.memory.concept}"]
        
        # Add character information
        context.append("## Characters")
        for char in self.memory.characters.values():
            context.append(f"- {char.name}: {', '.join(char.traits)}")
            if char.relationships:
                rel_text = "; ".join([f"{rel_type} with {rel}" for rel, rel_type in char.relationships.items()])
                context.append(f"  Relationships: {rel_text}")
        
        # Add recent plot events (last 3 episodes or less)
        context.append("## Recent Events")
        recent_events = [e for e in self.memory.plot_events if e.episode > episode - 3]
        for event in recent_events[-5:]:  # Last 5 events only
            context.append(f"- Episode {event.episode}: {event.description}")
        
        # Add world building info
        if self.memory.world_building.locations or self.memory.world_building.rules:
            context.append("## World Information")
            for loc_name in list(self.memory.world_building.locations.keys())[:3]:
                context.append(f"- Location: {loc_name}")
            for rule_name, rule in list(self.memory.world_building.rules.items())[:3]:
                context.append(f"- Rule: {rule_name}: {rule}")
        
        return "\n".join(context)
    
    def save_memory(self, filepath: str) -> None:
        """Save memory to file"""
        with open(filepath, "w") as f:
            f.write(self.memory.json())
    
    def load_memory(self, filepath: str) -> None:
        """Load memory from file"""
        with open(filepath, "r") as f:
            memory_data = json.load(f)
            self.memory = StoryMemory.parse_obj(memory_data)
