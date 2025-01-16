# ragtime-2-agentic
```
agentic-rag-project/
├── docker/
│   ├── api/
│   │   └── Dockerfile        # Dockerfile for Flask API service
│   ├── llm/
│   │   └── Dockerfile        # Dockerfile for local LLM service
│   ├── frontend/
│   │   └── Dockerfile        # Dockerfile for React frontend
│   └── db/
│       └── Dockerfile        # Dockerfile for PostgreSQL service
├── docker-compose.yml        # Compose file to orchestrate services
├── data/                     # Directory for local data and datasets
│   ├── Chunks                # Directory for generated embeddings
│   └── README.md             # (Optional) Instructions for data placement
├── src/                      # Source code for the RAG system
│   ├── flask_app/            # Flask server code
│   │   ├── __init__.py       # Initialize Flask app and extensions
│   │   ├── requirements.txt  # TODO: set requirements seperately for each container
│   │   ├── main.py           # Entry point for the Flask API
│   │   ├── db.py             # db calls
│   │   └── routes.py         # API route handlers organized by Blueprints
│   ├── rag_agent.py          # Core logic for the retrieval-augmented generation agent
│   ├── local_llm.py          # Wrappers or utilities for interacting with the local LLM
│   ├── retriever.py          # Code related to information retrieval (optional)
│   ├── utils.py              # Utility functions for the RAG agent
│   └── db_utils.py           # Database utility functions specific to RAG
├── frontend/
│   └── ...                   # React application source code
├── requirements.txt          # Python dependencies
├── README.md                 # Project overview, setup instructions, etc.
└── .gitignore                # Files and directories to ignore in version control
```


# Step 0: "Installing dependencies..."

```pip install -r requirements.txt```

need hugginface token to donwload model
huggingface-cli repo download answerdotai/ModernBERT-large --include config.json


# Step 1: Run the data generation script

Run data generator script...
```python3 ./data/generator.py```

# Step 2: Bring up Docker containers

Start Docker containerization
```docker-compose up -d```

# Step 3: Run the data ingestion script

Ingest JSON into Postgres container
```python3 ./data/ingest.py```

