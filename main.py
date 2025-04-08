# main.py
import os
import argparse
from api.openai_client import OpenAIClient
from api.perplexity_client import PerplexityClient
from memory.memory_manager import MemoryManager
from generator.story_planner import StoryPlanner
from generator.narrative_engine import NarrativeEngine
from dotenv import load_dotenv

# Add this line to load environment variables
load_dotenv()  

# Debug environment variables
print(f"OpenAI API Key loaded: {os.getenv('OPENAI_API_KEY') is not None}")
print(f"Perplexity API Key loaded: {os.getenv('PERPLEXITY_API_KEY') is not None}")


def select_api_client(api_choice, api_key=None):
    """Select and initialize API client based on user choice"""
    if api_choice.lower() == "openai":
        # First try command line arg, then environment variable
        return OpenAIClient(api_key=api_key)
    elif api_choice.lower() == "perplexity":
        return PerplexityClient(api_key=api_key)
    else:
        raise ValueError(f"Unsupported API choice: {api_choice}")

def main():
    parser = argparse.ArgumentParser(description='AI Story Generator')
    parser.add_argument('--concept', type=str, required=True, 
                        help='Story concept or prompt')
    parser.add_argument('--title', type=str, required=True, 
                        help='Story title')
    parser.add_argument('--episodes', type=int, default=3, 
                        help='Number of episodes to generate')
    parser.add_argument('--api', type=str, default='openai', 
                        choices=['openai', 'perplexity'],
                        help='API to use for generation')
    parser.add_argument('--output', type=str, default='output', 
                        help='Output directory')
    parser.add_argument('--api_key', type=str, help='API key to use')
    
    args = parser.parse_args()
    # Add this debug line
    print(f"Parsed arguments: {vars(args)}")

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    # Initialize API client
    api_client = select_api_client(args.api, args.api_key)
    
    # Initialize memory manager
    memory_manager = MemoryManager(api_client)
    memory_manager.initialize_memory(args.concept, args.title)
    
    # Initialize story planner
    story_planner = StoryPlanner(api_client)
    
    # Generate story blueprint
    print(f"Generating story blueprint for: {args.concept}")
    blueprint = story_planner.generate_blueprint(args.concept)
    
    # Save blueprint
    with open(os.path.join(args.output, "blueprint.txt"), "w") as f:
        f.write(blueprint)
    
    # Initialize narrative engine
    narrative_engine = NarrativeEngine(api_client, memory_manager)
    
    # Generate episodes
    for i in range(1, args.episodes + 1):
        print(f"Generating episode {i}...")
        
        # Get relevant context from memory
        context = memory_manager.get_relevant_context(i)
        
        # Generate episode
        episode = narrative_engine.generate_episode(
            args.concept, blueprint, context, i
        )
        
        # Save episode
        with open(os.path.join(args.output, f"episode_{i}.txt"), "w") as f:
            f.write(episode)
        
        # Save updated memory after each episode
        memory_manager.save_memory(os.path.join(args.output, "memory.json"))
        
        print(f"Episode {i} completed.")
    
    print(f"Story generation complete. Output saved to {args.output}/")

if __name__ == "__main__":
    main()
