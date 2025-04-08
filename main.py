# main.py
import os
import sys
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
    parser.add_argument('--concept', type=str, help='Story concept or prompt')
    parser.add_argument('--title', type=str, help='Story title')
    parser.add_argument('--episodes', type=int, default=3, help='Number of episodes to generate')
    parser.add_argument('--api', type=str, default='openai', choices=['openai', 'perplexity'], help='API to use for generation')
    parser.add_argument('--output', type=str, help='Output directory')
    parser.add_argument('--api_key', type=str, help='API key to use')
    parser.add_argument('--continue_story', action='store_true', help='Continue an existing story')
    
    args = parser.parse_args()
    
    # Interactive mode if no arguments provided
    if len(sys.argv) == 1 or args.continue_story:
        print("Welcome to AI Story Generator!")
        story_choice = input("Do you want to (1) Create a new story or (2) Continue an existing story? Enter 1 or 2: ")
        
        if story_choice == "1":
            # New story
            args.concept = input("Enter story concept: ")
            args.title = input("Enter story title: ")
            args.episodes = int(input("Enter number of episodes to generate: "))
            args.output = os.path.join("stories", input("Enter output folder name (will be saved under 'stories/'): "))
            args.api = input("Choose API (openai/perplexity): ").lower() or "openai"
        
        elif story_choice == "2":
            # Continue existing story
            args.continue_story = True
            # List available stories
            print("Available stories:")
            stories_dir = "stories"
            if not os.path.exists(stories_dir):
                print("No stories found.")
                return
                
            stories = [d for d in os.listdir(stories_dir) if os.path.isdir(os.path.join(stories_dir, d))]
            for i, story in enumerate(stories):
                print(f"{i+1}. {story}")
                
            story_idx = int(input("Enter the number of the story to continue: ")) - 1
            if story_idx < 0 or story_idx >= len(stories):
                print("Invalid selection.")
                return
                
            args.output = os.path.join(stories_dir, stories[story_idx])
            
            # Load existing memory
            memory_path = os.path.join(args.output, "memory.json")
            if not os.path.exists(memory_path):
                print(f"Memory file not found in {args.output}")
                return
                
            # Read blueprint
            blueprint_path = os.path.join(args.output, "blueprint.txt")
            if not os.path.exists(blueprint_path):
                print(f"Blueprint file not found in {args.output}")
                return
                
            with open(blueprint_path, "r") as f:
                blueprint = f.read()
                
            # Count existing episodes
            existing_episodes = len([f for f in os.listdir(args.output) if f.startswith("episode_") and f.endswith(".txt")])
            print(f"Found {existing_episodes} existing episodes.")
            
            args.episodes = int(input(f"How many additional episodes to generate? "))
            args.api = input("Choose API (openai/perplexity): ").lower() or "openai"
            
            # We'll set these later from the memory file
            args.concept = None
            args.title = None
    
    # Add this debug line
    print(f"Parsed arguments: {vars(args)}")

    # Create output directory if it doesn't exist
    if args.output:
        os.makedirs(args.output, exist_ok=True)
    else:
        print("Output directory is required.")
        return
    
    # Initialize API client
    api_client = select_api_client(args.api, args.api_key)
    
    # Initialize memory manager
    memory_manager = MemoryManager(api_client)
    
    # Check if continuing a story
    if story_choice == "2" if 'story_choice' in locals() else args.continue_story:
        # Load existing memory
        memory_manager.load_memory(os.path.join(args.output, "memory.json"))
        args.concept = memory_manager.memory.concept
        args.title = memory_manager.memory.title
        
        # Read blueprint
        with open(os.path.join(args.output, "blueprint.txt"), "r") as f:
            blueprint = f.read()
            
        # Count existing episodes
        existing_episodes = len([f for f in os.listdir(args.output) if f.startswith("episode_") and f.endswith(".txt")])
        start_episode = existing_episodes + 1
    else:
        # Initialize new memory
        memory_manager.initialize_memory(args.concept, args.title)
        
        # Initialize story planner
        story_planner = StoryPlanner(api_client)
        
        # Generate story blueprint
        print(f"Generating story blueprint for: {args.concept}")
        blueprint = story_planner.generate_blueprint(args.concept)
        
        # Save blueprint
        with open(os.path.join(args.output, "blueprint.txt"), "w") as f:
            f.write(blueprint)
            
        start_episode = 1
    
    # Initialize narrative engine
    narrative_engine = NarrativeEngine(api_client, memory_manager)
    
    # Generate episodes
    for i in range(start_episode, start_episode + args.episodes):
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
