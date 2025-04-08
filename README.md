# AI Story Generator - Dual LLM Architecture for Long-Form Storytelling


An innovative AI-driven storytelling pipeline that generates multi-episode stories with consistent characters, plots, and world-building elements, overcoming the traditional token and context limitations of large language models.

## Table of Contents

- [Introduction](#introduction)
- [Architecture](#architecture)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Run the Application](#run-the-application)
- [Example Usage](#example-usage)
- [Project Structure](#project-structure)
- [Memory System](#memory-system)
- [Future Improvements](#future-improvements)
- [License](#license)


## Introduction

The AI Story Generator leverages a powerful Dual LLM Architecture to create expansive, multi-episode narratives that maintain character consistency, plot coherence, and world-building integrity across unlimited episodes. Traditional LLMs struggle with long-form content due to context window limitations, often resulting in discontinuities and contradictions across a story's timeline. Our solution implements a specialized memory management system and dedicated LLMs for different aspects of the storytelling process.

This project was developed as part of the KUKU FM Hackathon Challenge 3: AI-based story creation.

## Architecture

### Dual LLM Architecture

Our system employs two specialized LLMs that work in tandem:

1. **Generator LLM**: Focuses on creative narrative production, crafting engaging scenes and dialogue.
2. **Memory Manager LLM**: Specializes in context tracking, consistency checking, and information extraction.

Dual LLM Architecture

### Information Flow Pipeline

1. **Blueprint Generation**: Creates the overall story structure.
2. **Context Assembly**: Retrieves relevant information from memory.
3. **Narrative Generation**: Produces story episodes with Generator LLM.
4. **Memory Extraction**: Extracts key elements from generated text.
5. **Memory Updates**: Maintains the three-tier memory structure.
6. **Context Compression**: Optimizes token usage for next episodes.

## Key Features

- **Multi-Episode Story Generation**: Create stories with unlimited episodes that maintain continuity.
- **Character Consistency**: Track character traits, relationships, and development across episodes.
- **Three-Tier Memory Structure**: Store and retrieve character vectors, plot events, and world-building elements.
- **Vector-Based Retrieval**: Use semantic similarity to retrieve the most relevant context.
- **Context Compression**: Reduce token usage while preserving critical information.
- **Consistency Checking**: Automatically identify and fix narrative inconsistencies.
- **Web Interface**: User-friendly interface for story creation and browsing.
- **CLI Support**: Command-line interface for automation and scripting.


## Technologies Used

- **Python**: Core programming language
- **LLM APIs**:
    - OpenAI API (GPT-4/3.5)
    - Perplexity API
    - Gemini API (prepared for future integration)
- **Sentence Transformers**: For vector embeddings and semantic search
- **Flask**: Web application framework
- **Pydantic**: Data validation and schema definition
- **TikToken**: Token counting for LLM inputs
- **Bootstrap**: Frontend styling for the web interface


## Installation

1. Clone the repository:
```bash
git clone https://github.com/soumysuwas/story_generator1.git
cd story_generator1
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Set up your API keys:
Create a `.env` file in the root directory and add your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
PERPLEXITY_API_KEY=your_perplexity_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```


## Run the Application

The AI Story Generator can be run in multiple ways:

### Web Interface

For a user-friendly graphical interface:

```bash
python -m web_app
```

This will start a Flask web server that you can access at http://127.0.0.1:5000/ in your browser.

### Interactive Command Line

For an interactive command-line experience:

```bash
python -m main
```

This will guide you through creating a new story or continuing an existing one via text prompts.

### Non-Interactive Command Line

For automated or scripted usage:

```bash
python -m main --concept "A space explorer discovers a hidden civilization on a supposedly uninhabited planet" --title "Hidden World" --episodes 3 --api openai --output stories/hidden_world
```

Parameters:

- `--concept`: The story concept or prompt
- `--title`: The story title
- `--episodes`: Number of episodes to generate (default: 3)
- `--api`: API to use for generation (openai or perplexity)
- `--output`: Output directory for story files
- `--continue_story`: Flag to continue an existing story


## Example Usage

### Creating a New Story (CLI)

```bash
python -m main --concept "A race between all the animals in the amazon forest." --title "Amazon Forest Race" --episodes 3 --api openai --output stories/amazon_race
```


### Creating a New Story (Web)

1. Access the web interface at http://127.0.0.1:5000/
2. Click "Create a New Story"
3. Enter story concept, title, number of episodes, and select API
4. Click "Generate Story"

### Continuing an Existing Story (CLI)

```bash
python -m main --continue_story --output stories/amazon_race --episodes 2 --api openai
```


### Continuing an Existing Story (Web)

1. Access the web interface at http://127.0.0.1:5000/
2. Click "Continue an Existing Story"
3. Select the story from the dropdown
4. Enter number of additional episodes and select API
5. Click "Continue Story"

## Project Structure

```
story_generator/
├── main.py                 # Entry point for CLI
├── web_app.py              # Web application
├── api/
│   ├── __init__.py
│   ├── openai_client.py    # OpenAI API wrapper
│   ├── memory_llm.py       # Specialized LLM for memory tasks
│   ├── perplexity_client.py # Perplexity API wrapper  
│   └── gemini_client.py    # Gemini API wrapper (prepared)
├── memory/
│   ├── __init__.py
│   ├── memory_manager.py   # Memory management system
│   ├── vector_store.py     # Vector embeddings for retrieval
│   └── schema.py           # Memory data structures
├── generator/
│   ├── __init__.py
│   ├── story_planner.py    # Blueprint generation
│   └── narrative_engine.py # Episode generation
├── utils/
│   ├── __init__.py
│   ├── prompts.py          # System prompts 
│   ├── context_compressor.py # Token optimization
│   └── token_counter.py    # Token usage tracking
├── evaluation/
│   ├── __init__.py
│   └── consistency_checker.py # Verify story coherence
├── templates/              # Web UI templates
├── stories/                # Generated stories folder
└── README.md
```


## Memory System

Our system implements a sophisticated three-tier memory structure:

### 1. Character Vectors

- Character traits, abilities, and motivations
- Relationship network and evolution
- Character development tracking


### 2. Plot Events Graph

- Chronological event timeline
- Causal connections between events
- Episode-specific event tracking


### 3. World-Building Repository

- Locations and their descriptions
- Rules and systems of the story world
- Objects and items of significance

The memory system uses vector embeddings for efficient retrieval of the most relevant context for each new episode generation, ensuring narrative coherence while managing token usage.

## Future Improvements

- Gemini API integration for enhanced performance
- Fine-tuning specialized LLMs for memory management
- Advanced visualization of the story memory map
- Multi-language support for global storytelling
- Audio narration generation from the text story
- Character illustration generation


## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Built with ❤️ for the KUKU FM Hackathon by the AI Story Generation Team
