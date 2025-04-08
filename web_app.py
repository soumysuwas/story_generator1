from flask import Flask, render_template, request, redirect, url_for
import threading
import os
import sys
from api.openai_client import OpenAIClient
from api.perplexity_client import PerplexityClient
from memory.memory_manager import MemoryManager
from generator.story_planner import StoryPlanner
from generator.narrative_engine import NarrativeEngine
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# Debug environment variables
print(f"OpenAI API Key loaded: {os.getenv('OPENAI_API_KEY') is not None}")
print(f"Perplexity API Key loaded: {os.getenv('PERPLEXITY_API_KEY') is not None}")

def select_api_client(api_choice, api_key=None):
    """Select and initialize API client based on user choice"""
    if api_choice.lower() == "openai":
        return OpenAIClient(api_key=api_key)
    elif api_choice.lower() == "perplexity":
        return PerplexityClient(api_key=api_key)
    else:
        raise ValueError(f"Unsupported API choice: {api_choice}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_story')
def new_story():
    return render_template('new_story.html')

@app.route('/continue_story')
def continue_story():
    # List available stories
    stories_dir = "stories"
    if not os.path.exists(stories_dir):
        return render_template('continue_story.html', stories=[], error="No stories found.")
        
    stories = [d for d in os.listdir(stories_dir) if os.path.isdir(os.path.join(stories_dir, d))]
    return render_template('continue_story.html', stories=stories)

@app.route('/generate_story', methods=['POST'])
def generate_story():
    if request.form.get('story_type') == 'new':
        # New story
        concept = request.form.get('concept')
        title = request.form.get('title')
        episodes = int(request.form.get('episodes'))
        output = request.form.get('output')
        api = request.form.get('api')
        
        # Create output directory
        output_path = os.path.join("stories", output)
        os.makedirs(output_path, exist_ok=True)
        
        # Initialize API client
        api_client = select_api_client(api)
        
        # Initialize memory manager
        memory_manager = MemoryManager(api_client)
        memory_manager.initialize_memory(concept, title)
        
        # Initialize story planner
        story_planner = StoryPlanner(api_client)
        
        # Generate story blueprint
        blueprint = story_planner.generate_blueprint(concept)
        
        # Save blueprint
        with open(os.path.join(output_path, "blueprint.txt"), "w") as f:
            f.write(blueprint)
            
        # Initialize narrative engine
        narrative_engine = NarrativeEngine(api_client, memory_manager)
        
        # Generate episodes
        progress = []
        for i in range(1, episodes + 1):
            progress.append(f"Generating episode {i}...")
            
            # Get relevant context from memory
            context = memory_manager.get_relevant_context(i)
            
            # Generate episode
            episode = narrative_engine.generate_episode(
                concept, blueprint, context, i
            )
            
            # Save episode
            with open(os.path.join(output_path, f"episode_{i}.txt"), "w") as f:
                f.write(episode)
            
            # Save updated memory after each episode
            memory_manager.save_memory(os.path.join(output_path, "memory.json"))
            
            progress.append(f"Episode {i} completed.")
        
        progress.append(f"Story generation complete. Output saved to {output_path}/")
        return render_template('result.html', progress=progress, story_path=output_path)
    
    else:
        # Continue existing story
        story_idx = int(request.form.get('story_idx'))
        episodes = int(request.form.get('episodes'))
        api = request.form.get('api')
        
        # List available stories
        stories_dir = "stories"
        stories = [d for d in os.listdir(stories_dir) if os.path.isdir(os.path.join(stories_dir, d))]
        
        output_path = os.path.join(stories_dir, stories[story_idx])
        
        # Initialize API client
        api_client = select_api_client(api)
        
        # Initialize memory manager
        memory_manager = MemoryManager(api_client)
        
        # Load existing memory
        memory_manager.load_memory(os.path.join(output_path, "memory.json"))
        concept = memory_manager.memory.concept
        title = memory_manager.memory.title
        
        # Read blueprint
        with open(os.path.join(output_path, "blueprint.txt"), "r") as f:
            blueprint = f.read()
            
        # Count existing episodes
        existing_episodes = len([f for f in os.listdir(output_path) if f.startswith("episode_") and f.endswith(".txt")])
        start_episode = existing_episodes + 1
        
        # Initialize narrative engine
        narrative_engine = NarrativeEngine(api_client, memory_manager)
        
        # Generate episodes
        progress = []
        for i in range(start_episode, start_episode + episodes):
            progress.append(f"Generating episode {i}...")
            
            # Get relevant context from memory
            context = memory_manager.get_relevant_context(i)
            
            # Generate episode
            episode = narrative_engine.generate_episode(
                concept, blueprint, context, i
            )
            
            # Save episode
            with open(os.path.join(output_path, f"episode_{i}.txt"), "w") as f:
                f.write(episode)
            
            # Save updated memory after each episode
            memory_manager.save_memory(os.path.join(output_path, "memory.json"))
            
            progress.append(f"Episode {i} completed.")
        
        progress.append(f"Story generation complete. Output saved to {output_path}/")
        return render_template('result.html', progress=progress, story_path=output_path)

@app.route('/view_story/<path:story_path>')
def view_story(story_path):
    # Get all episode files
    episode_files = [f for f in os.listdir(story_path) if f.startswith("episode_") and f.endswith(".txt")]
    episode_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
    
    episodes = []
    for file in episode_files:
        with open(os.path.join(story_path, file), 'r') as f:
            content = f.read()
            episodes.append({'title': file, 'content': content})
    
    # Get blueprint
    blueprint = ""
    blueprint_path = os.path.join(story_path, "blueprint.txt")
    if os.path.exists(blueprint_path):
        with open(blueprint_path, 'r') as f:
            blueprint = f.read()
    
    return render_template('view_story.html', episodes=episodes, blueprint=blueprint, story_path=story_path)

@app.route('/browse_stories')
def browse_stories():
    stories_dir = "stories"
    if not os.path.exists(stories_dir):
        return render_template('browse_stories.html', stories=[], error="No stories found.")
        
    stories = []
    for story_name in os.listdir(stories_dir):
        story_path = os.path.join(stories_dir, story_name)
        if os.path.isdir(story_path):
            # Count episodes
            episode_count = len([f for f in os.listdir(story_path) if f.startswith("episode_") and f.endswith(".txt")])
            
            # Get title and concept if available
            title = story_name
            concept = ""
            memory_path = os.path.join(story_path, "memory.json")
            if os.path.exists(memory_path):
                try:
                    with open(memory_path, 'r') as f:
                        memory_data = json.load(f)
                        title = memory_data.get('title', story_name)
                        concept = memory_data.get('concept', "")
                except:
                    pass
                    
            stories.append({
                'path': story_path,
                'name': story_name,
                'title': title,
                'concept': concept,
                'episodes': episode_count
            })
            
    return render_template('browse_stories.html', stories=stories)

def shutdown_server():
    """Shutdown the server after a brief delay"""
    def shutdown_function():
        # Give the server 1 second to send the response
        import time
        time.sleep(1)
        os._exit(0)
    
    # Start shutdown in a separate thread
    threading.Thread(target=shutdown_function).start()
    return 'Server shutting down...'

@app.route('/shutdown')
def shutdown():
    return shutdown_server()

if __name__ == '__main__':
    app.run(debug=True)
