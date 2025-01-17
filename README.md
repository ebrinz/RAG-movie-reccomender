# ragtime-2-agentic

```
######################################################################################
#                              Project Structure                                     #
######################################################################################

agentic-rag-project/
│
├── src/                      
│   ├── api/                           # Flask server code
│   │   ├── __init__.py                # Initialize Flask app and extensions
│   │   ├── requirements.txt           # Dependencies for Flask server
│   │   ├── main.py                    # Entry point for the Flask API
│   │   ├── db.py                      # Database calls
│   │   ├── routes.py                  # API route handlers organized by Blueprints
│   │   ├── model_utils.py             # Utilities for SQL queries and model management
│   │   └── Dockerfile                 # Dockerfile for Flask API service
│   ├── llm/                           # LLM-related code and configurations
│   │   └── Dockerfile                 # Dockerfile for LLM service
│   ├── ui/                            # Frontend UI code
│   │   ├── public/                    #         
│   │   │   └── index.html             # HTML template
│   │   ├── src/                       #         
│   │   │   ├── components/            # 
│   │   │   │   ├── App.js             # Main App component
│   │   │   │   ├── PromptInput.js     # Component for prompt input
│   │   │   │   ├── ResponseList.js    # Component for displaying responses
│   │   │   │   └── SimilarMovies.js   # Component for displaying similar movies
│   │   │   ├── api.js                 # API utility functions for UI
│   │   │   ├── helpers/               # Helper functions and custom hooks
│   │   │   │   └── handleSubmit.js    # Logic for handling submissions
│   │   │   ├── styles/                # Stylesheets
│   │   │   │   └── index.css          # Main CSS file
│   │   │   └── index.js               # Entry point for React application
│   │   ├── package.json               #
│   │   ├── package-lock.json          #
│   │   └── Dockerfile                 # Dockerfile for React service
│   └── db/                            # Database-related scripts and configurations
│       ├── Dockerfile                 # Dockerfile for Postgres service
│       └── data/                      # Directory for local data and datasets
│           ├── chunks/                # Directory for generated embeddings
│           ├── generator.py           # Script for creating embeddings from data
│           ├── ingest.py              # Script for inputting data from chunks into db
│           └── README.md              # Instructions for data placement
│                                      #
├── build/                             # Directory for UI build output
│   └── ...                            # Compiled React application files
├── docker-compose.yml                 # Compose file to orchestrate services
├── requirements.txt                   # Global Python dependencies for the project
├── README.md                          # Project overview, setup instructions, etc.
└── .gitignore                         # Files and directories to ignore in version control

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
