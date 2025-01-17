# ragtime-2-agentic

```
agentic-rag-project/
│
├── src/                      # Source code for the RAG system
│   ├── api/                  # Flask server code
│   │   ├── __init__.py       # Initialize Flask app and extensions
│   │   ├── requirements.txt  # TODO: set requirements seperately for each container
│   │   ├── main.py           # Entry point for the Flask API
│   │   ├── db.py             # db calls
│   │   ├── routes.py         # API route handlers organized by Blueprints
│   │   ├── model_utils.py    # SQL queries
│   │   └── Dockerfile        # Dockerfile for Flask API service
│   ├── llm/                  # llm stuff and code
│   │   └── Dockerfile        # TODO: Get Ollama running Llama3 without manually starting
│   ├── ui/                   # ui code
│   │   └──  public/          #
│   │   │    └── index.html   #
│   │   ├── src/              #
│   │   │   ├── index.js      #
│   │   │   ├── App.js        #
│   │   │   └── api.js        #
│   │   ├── package.json      #
│   │   └── package-lock.json #
│   │   └── Dockerfile        # Dockerfile for React service
│   └── db/                   # Database
│       ├── Dockerfile        # Dockerfile for Postgres service
│       └── data/             # Directory for local data and datasets
│           ├── chunks/       # Directory for generated embeddings
│           ├── generator.py  # Creating embeddings from data file
│           ├── ingest.py     # Script for inputing data from Chunks/ into db
│           └── README.md     # Instructions for data placement
├── build/                    # Directory for ui build
│   └── ...                   # React application source code
├── docker-compose.yml        # Compose file to orchestrate services
├── requirements.txt          # Python dependencies
├── README.md                 # Project overview, setup instructions, etc.
└── .gitignore                # Files and directories to ignore in version control
```


# Step 0: "Installing dependencies..."

```pip install -r requirements.txt```

# Step 1: Run the data generation script

Run data generator script...
```python3 ./src/db/data/generator.py```

# Step 2: Bring up Docker containers

Start Docker containerization
```docker-compose up -d```

# Step 3: Run the data ingestion script

Ingest JSON into Postgres container
```python3 ./src/db/data/ingest.py```



src/
├── components/
│   ├── App.js
│   ├── PromptInput.js
│   ├── ResponseList.js
│   └── SimilarMovies.js
├── api/
│   └── index.js        (formerly api.js, or keep as api.js here)
├── helpers/
│   └── handleSubmit.js (if separated later)
├── styles/
│   └── index.css       (or keep index.css at root if preferred)
├── index.js