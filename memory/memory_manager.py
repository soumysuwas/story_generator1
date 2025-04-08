# memory_manager.py
import json
from .schema import StoryMemory, Character, PlotEvent
from api.openai_client import OpenAIClient
from typing import Dict, List, Any

class MemoryManager:
    def __init__(self, api_client):
        self.api_client = api_client
        self.memory = None
        self.extraction_prompt = """
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
    
    def initialize_memory(self, concept: str, title: str) -> None:
        self.memory = StoryMemory(title=title, concept=concept)
    
    def extract_story_elements(self, story_text: str) -> Dict[str, Any]:
        """Extract story elements from generated text using LLM"""
        response = self.api_client.generate_text(
            system_prompt=self.extraction_prompt,
            user_input=f"Extract story elements from this text:\n{story_text}"
        )
        try:
            # Parse the returned JSON
            extracted = json.loads(response)
            return extracted
        except json.JSONDecodeError:
            print("Error parsing JSON from extraction response")
            return {}
    
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
