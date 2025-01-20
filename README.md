# RAG-movie-recommender: Experimentation with Retrieval-Augmented Generation

This project explores Retrieval-Augmented Generation (RAG), an common technique that combines retrieval-based and generative AI systems. The primary focus is to experiment with RAG's ability to generate accurate, contextually rich responses by leveraging both embedding models and generative architectures. In this case, the domain of movies is used, with a dataset of film plots serving as the knowledge base.

### Dataset Overview
The project utilizes the [Wiki-Movie-Plots dataset](https://www.kaggle.com/datasets/jrobischon/wikipedia-movie-plots) — a collection of movie metadata and plot summaries sourced from Wikipedia and other resources. Movies not marked as "American" or released before 1950 are discluded in database.

### Goals and Use Case
The primary goal is to assess various RAG configurations in terms of embedding generation, retrieval, and response generation. This encompasses several practical and educational objectives:

#### Learning How to Use RAG
- **Hands-On Experimentation:** By working with movie plots, practitioners learn how to implement RAG pipelines—from generating embeddings to retrieving relevant and common-sense documents.
- **Understanding Workflow:** The project provides insight into integrating embedding models with generative AI, familiarizing users with the nuances of RAG system design and tuning.

#### Hypothetical Document Extraction
- **Simulated Extraction:** The system can hypothetically extract relevant movie plot information based on user queries, demonstrating how RAG can be applied to document extraction tasks beyond movie recommendations.
- **Contextual Responses:** Augmented generation uses retrieved plot summaries to form answers, illustrating RAG's potential in synthesizing coherent responses from multiple document sources.

#### Evaluating Embedding Similarity
- **Similarity Metrics:** The project employs similarity measures (e.g., cosine similarity) to identify and retrieve the most relevant movie plots corresponding to a given query.
- **Quality Assessment:** By analyzing which retrieved documents are most similar to the query, the project evaluates the effectiveness of different embedding models and similarity metrics in capturing semantic relevance.

---

# GETTING STARTED

## 1: Environment
##### Make sure the following are present on host machine
```
docker.io or Docker Desktop app
docker-compose
```

## 2: Parameters
##### Adjust .env for embedding chosen model and embedding model's output vector size


## 3: Bring up Docker containers

##### Bringup scripts: build up data ingest pull
```make all```

##### Build Docker Compose stack
```make build```

##### Start Docker Compose stack and detach
```make up```

##### Download data and create embeddings
```make data```

##### Ingest data into the database
```make ingest```

##### Pull the Llama3 model
```make pull```

##### Show logs and folllow of all containers
```make logs```

##### Stop Docker Compose stack
```make down```

##### Stop and clean up the Docker Compose stack
```make clean```

##### Clear the Docker environment
```make desolate```

##### Offload chnuks into local storage and free up dir for new model embeddings
```make room```


## 4: Load page
##### Served for browser at
```http://localhost:3000/```
or
```make open```


## Sitemap
```
│
├── Makefile
├── README.md
├── data
│   ├── artifacts
│   │   └── /
│   └── chunks
│       └── /
├── docker-compose.yml
└── src
    ├── api
    │   ├── Dockerfile
    │   ├── README.md
    │   ├── __init__.py
    │   ├── build.py
    │   ├── db.py
    │   ├── ingest.py
    │   ├── main.py
    │   ├── model_utils.py
    │   ├── requirements.txt
    │   └── routes.py
    ├── db
    │   └──  Dockerfile
    ├── llm
    │   ├── Dockerfile
    │   └── README.md
    └── ui
        ├── Dockerfile
        ├── README.md
        ├── nodemon.json
        ├── package-lock.json
        ├── package.json
        ├── public
        │   └── index.html
        └── src
            ├── api
            │   └── api.js
            ├── components
            │   ├── App.js
            │   ├── EllipsisLoader.js
            │   ├── PromptInput.js
            │   ├── ResponseList.js
            │   ├── SimilarMovies.js
            │   └── TopBilling.js
            ├── helpers
            │   └── useSubmitHandler.js
            ├── index.js
            └── styles
                ├── EllipsisLoader.css
                ├── TopBilling.css
                ├── index.css
                └── terminal.css
```

## TODOS

- [ ] UI: Eliminate ui console warning
- [ ] API: Remove db data files and dir - maybe leave dummy data
- [ ] API: troubleshoot possible embeddings mismatch
- [ ] API: Explore and log embedding evals for different models
- [ ] API: Explore fine tuning
- [ ] API: Use Flask API at :80 to serve metrics
- [ ] UI: Bring llm output into into text field as pseudo terminal

