# schema.py
from typing import Dict, List, Optional, Any
from pydantic import BaseModel

class Character(BaseModel):
    id: str
    name: str
    traits: List[str] = []
    relationships: Dict[str, str] = {}
    development: List[Dict[str, Any]] = []
    
class PlotEvent(BaseModel):
    id: str
    episode: int
    scene: Optional[int]
    description: str
    characters_involved: List[str] = []
    consequences: List[str] = []
    
class WorldBuilding(BaseModel):
    locations: Dict[str, Dict[str, Any]] = {}
    rules: Dict[str, str] = {}
    objects: Dict[str, Dict[str, Any]] = {}
    
class StoryMemory(BaseModel):
    title: str
    concept: str
    characters: Dict[str, Character] = {}
    plot_events: List[PlotEvent] = []
    world_building: WorldBuilding = WorldBuilding()
    current_episode: int = 0
