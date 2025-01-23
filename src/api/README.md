

# Some exmaple CURLS for test

### Movie title lookup
```
curl "http://localhost:5000/movies?title=star&limit=5&offset=5"
```

### Movie title paginated
```
curl "http://localhost:5000/movies?title=star%20wars&limit=5&offset=5"
```

### Vector search with cosine similarity
```
curl -X POST http://localhost:5000/vector_search \
-H "Content-Type: application/json" \
-d '{
    "text": "science fiction adventure",
    "num_neighbors": 5,
    "metric": "cosine",
    "use_normalized": true,
    "min_similarity": 0.5
}'
```

### Hybrid search combining embedding and text
```
curl -X POST http://localhost:5000/hybrid_search \
-H "Content-Type: application/json" \
-d '{
    "text": "space adventure",
    "text_query": "alien spacecraft",
    "num_neighbors": 5,
    "metric": "cosine",
    "embedding_weight": 0.7,
    "min_similarity": 0.5
}'
```


### ollama task

```
curl http://localhost:5000/generate \
-H "Content-Type: application/json" \
-d '{
  "prompt": "energon"
}'
```