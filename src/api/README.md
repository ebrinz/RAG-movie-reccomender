

### Some exmaple CURLS for test

```
curl "http://localhost:5000/movies?limit=5&title=In"
```

```
curl -X POST http://localhost:5000/vector_search \
-H "Content-Type: application/json" \
-d '{
    "text": "A mind-bending sci-fi thriller about dreams within dreams",
    "num_neighbors": 3
}'
```
