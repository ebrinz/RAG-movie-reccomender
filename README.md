# RAG-movie-recommender: Experimentation with Retrieval-Augmented Generation

This project explores **Retrieval-Augmented Generation (RAG)**, an advanced technique in the intersection of **retrieval-based** and **generative AI systems**. The primary focus is to experiment with RAG's ability to generate accurate and contextually rich responses by leveraging both embedding models and generative architectures. Specifically, this project aims to apply RAG techniques in the domain of movies, using a dataset of film plots as the knowledge base.

## Dataset Overview

The project utilizes the [Wiki-Movie-Plots dataset](https://huggingface.co/datasets/vishnupriyavr/wiki-movie-plots-with-summaries/resolve/main/wiki_movie_plots_deduped_with_summaries.csv), which is a collection of movie metadata and plot summaries sourced from Wikipedia and other resources. The dataset contains details for a large number of movies, including:

- **Title**: The name of the movie.
- **Release Year**: The year the movie was released.
- **Origin/Ethnicity**: The country or cultural origin of the film.
- **Director**: The director(s) of the film.
- **Cast**: Key actors and actresses in the movie.
- **Genre**: The genre(s) associated with the movie.
- **Wiki Page**: The URL for the Wikipedia page.
- **Plot**: A detailed plot summary of the movie.

### Dataset Filtering
To ensure succinctness and relevance for experimentation:
1. **Cultural Scope**: Only movies with an origin/ethnicity marked as **"American"** are included.
2. **Temporal Scope**: Only movies released **after 1950** are considered.

These filters were applied to reduce the dataset size and to focus on more modern, culturally specific films for ease of processing and analysis.

## Goals and Use Case

The primary goal of this project is to assess the efficacy of various RAG configurations in embedding generation, retrieval, and response generation using the filtered dataset. Specifically:

1. **Embedding Generation**:
   - Create dense vector representations (embeddings) of the movie plot summaries using pre-trained models.
   - Store these embeddings for efficient similarity-based retrieval.

2. **Similarity-Based Retrieval**:
   - Use similarity metrics (e.g., cosine similarity) to identify and retrieve the most relevant movie plots based on a user-provided query.

3. **Augmented Generation**:
   - Employ generative AI models to craft responses or summaries augmented with the retrieved plot information.

## Why American Movies Post-1950?

- **Cultural Relevance**: Post-1950 American cinema represents a significant portion of global film output, offering a wide variety of genres and storytelling styles.
- **Data Conciseness**: Filtering by this criterion ensures the dataset is manageable for experimentation without sacrificing diversity in content.
- **Temporal Modernity**: Modern movies have plots and themes that align better with contemporary language models' training data.

## Applications

- **Movie Recommendations**: Generate personalized movie suggestions based on user preferences or queries.
- **Content Summarization**: Provide brief and contextually accurate plot summaries.
- **Research & Analysis**: Analyze trends in film genres, storytelling techniques, and cultural shifts over time.

This project provides a solid foundation for exploring the intersection of retrieval systems, natural language understanding, and generative AI, with real-world applications in entertainment, research, and recommendation systems.


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
├── README.md
├── build
├── docker-compose.yml
├── playbook.yml
├── requirements.txt
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
    │   ├── Dockerfile
    │   └── data
    │       ├── README.md
    │       ├── generator.py
    │       ├── ingest.py
    │       └── movie_embeddings.json
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

