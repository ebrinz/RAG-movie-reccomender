```
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

## GETTING STARTED

##### Step 1: Bring up Docker containers
Adjust .env for embedding chosen model and embedding model's output vector size

##### Step 2: Bring up Docker containers
Make sure the following are present on host machine
```
docker.io or Docker Desktop app
docker-compose
Ansible
```

##### Step 3: Bring up Docker containers
Start Docker containerization
```ansible-playbook playbook.yml```


## TODOS
- [ ] Move Reqs into api
- [ ] Eliminate console warning
- [ ] Remove db data files and dir - maybe leave dummy data

