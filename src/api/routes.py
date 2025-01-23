from flask import Blueprint, jsonify, request, Response
import requests
from logger import logger
from db import fetch_movies, fetch_similar_movies, search_movies_hybrid
from model_utils import get_embedding, load_model
import numpy as np

api_bp = Blueprint('api', __name__, url_prefix='/')
tokenizer, model, device = load_model()

@api_bp.route('/debug', methods=['POST'])
def debug_request():
    try:
        logger.info(f"Raw request data: {request.data}")
        data = request.get_json(force=True)
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error in /debug: {e}")
        return jsonify({"error": str(e)}), 400

@api_bp.route('/movies', methods=['GET'])
def get_movies():
    try:
        limit = request.args.get('limit', default=10, type=int)
        offset = request.args.get('offset', default=0, type=int)
        title_filter = request.args.get('title', default="", type=str)
        if limit < 1:
            return jsonify({"error": "Limit must be greater than 0"}), 400
        if offset < 0:
            return jsonify({"error": "Offset must be non-negative"}), 400
        logger.info(f"Fetching movies with limit={limit}, offset={offset}, title_filter='{title_filter}'")
        movies = fetch_movies(
            limit=limit,
            offset=offset,
            title_filter=title_filter
        )
        return jsonify({
            "movies": movies,
            "metadata": {
                "limit": limit,
                "offset": offset,
                "title_filter": title_filter if title_filter else None,
                "count": len(movies)
            }
        })
    except Exception as e:
        logger.error(f"Error fetching movies: {e}", exc_info=True)
        return jsonify({"error": f"Unable to fetch movies: {e}"}), 500

@api_bp.route('/vector_search', methods=['POST'])
def vector_search():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        text = data.get('text')
        if not text:
            return jsonify({"error": "Text is required"}), 400
        num_neighbors = int(data.get('num_neighbors', 10))
        metric = data.get('metric', 'cosine')
        use_normalized = bool(data.get('use_normalized', True))
        min_similarity = float(data.get('min_similarity', 0.0))
        logger.info(f"Vector search request - text: '{text}', metric: {metric}, neighbors: {num_neighbors}")
        try:
            embedding = get_embedding(text, tokenizer, model, device)
            if isinstance(embedding, np.ndarray):
                embedding = embedding.tolist()
            logger.info(f"Generated embedding of length: {len(embedding)}")
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}", exc_info=True)
            return jsonify({"error": "Failed to generate embedding"}), 500
        results = fetch_similar_movies(
            embedding=embedding,
            num_neighbors=num_neighbors,
            metric=metric,
            use_normalized=use_normalized,
            min_similarity=min_similarity
        )
        return jsonify({
            "results": results,
            "query": text,
            "metric": metric,
            "embedding_type": "normalized" if use_normalized else "original",
            "num_results": len(results)
        })
    except Exception as e:
        logger.error(f"Error in vector_search endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@api_bp.route('/hybrid_search', methods=['POST'])
def hybrid_search():
    try:
        data = request.json
        text = data.get('text')
        text_query = data.get('text_query', '')
        num_neighbors = data.get('num_neighbors', 10)
        metric = data.get('metric', 'cosine')
        use_normalized = data.get('use_normalized', True)
        embedding_weight = data.get('embedding_weight', 0.7)
        min_similarity = data.get('min_similarity', 0.0)
        if not text:
            return jsonify({"error": "Text for embedding is required"}), 400
        if metric not in ['cosine', 'euclidean']:
            return jsonify({"error": "Invalid metric. Must be 'cosine' or 'euclidean'"}), 400
        if not 0 <= embedding_weight <= 1:
            return jsonify({"error": "embedding_weight must be between 0 and 1"}), 400
        logger.info(f"Performing hybrid search with {metric} metric")
        embedding = get_embedding(text, tokenizer, model, device)
        results = search_movies_hybrid(
            embedding=embedding,
            text_query=text_query,
            num_neighbors=num_neighbors,
            metric=metric,
            use_normalized=use_normalized,
            embedding_weight=embedding_weight,
            min_similarity=min_similarity
        )
        return jsonify({
            "results": results,
            "embedding_query": text,
            "text_query": text_query,
            "metric": metric,
            "embedding_weight": embedding_weight
        })
    except Exception as e:
        logger.error(f"Error in hybrid search: {e}", exc_info=True)
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@api_bp.route('/generate', methods=['POST'])
def generate_prompt():
    try:
        data = request.json
        logger.info(f"data: {data}")
        prompt = data.get('prompt', "too many puppies?")
        num_ctx = data.get('num_ctx', 512)
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
        response = requests.post(
            "http://llm:11434/api/chat",
            json={
                "model": "llama3",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "The system is a movie producer who crafts creative and engaging plots. "
                            "The system creates a plot summary meant to pitch to a director. The system uses the "
                            "terms provided by the user to create a plot summary in 50 tokens or less. "
                            "No intro, just plain summary of the plot."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"{prompt}"
                    }
                ],
                "options": {
                    "num_ctx": f"{num_ctx}",
                    "temperature": 1.2,
                    "num_predict": 255,
                    "top_k": 80,
                    "top_p": 0.9,
                    "min_p": 0.7
                }
            },
            headers={"Content-Type": "application/json"},
            stream=True
        )
        if response.status_code != 200:
            return jsonify({"error": f"LLM service returned an error: {response.text}"}), response.status_code
        def generate():
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    yield chunk.decode('utf-8')
        return Response(generate(), content_type='application/json')
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500