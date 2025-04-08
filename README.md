

##  Project Structure
```
story_generator/
├── main.py                 # Entry point
├── api/
│   ├── __init__.py
│   ├── openai_client.py    # OpenAI API wrapper
│   ├── perplexity_client.py # Perplexity API wrapper  
│   └── gemini_client.py    # Gemini API wrapper (future)
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
│   └── token_counter.py    # Token usage tracking
├── evaluation/
│   ├── __init__.py
│   └── consistency_checker.py # Verify story coherence
├── stories/
│   ├── story1/#folder name can be different for diffeent stories based on the user prompt
│   ├── story2/
│   └── story3/
└── README.md
```