from flask import Blueprint, jsonify, request, Response
import requests  # For making HTTP requests to the LLM service
import logging
from db import fetch_movies, fetch_similar_movies
from model_utils import get_embedding

api_bp = Blueprint('api', __name__, url_prefix='/')

@api_bp.route('/debug', methods=['POST'])
def debug_request():
    try:
        logging.info(f"Raw request data: {request.data}")
        data = request.get_json(force=True)
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error in /debug: {e}")
        return jsonify({"error": str(e)}), 400


@api_bp.route('/movies', methods=['GET'])
def get_movies():
    try:
        limit = request.args.get('limit', default=10, type=int)
        title_filter = request.args.get('title', default="", type=str)
        movies = fetch_movies(limit=limit, title_filter=title_filter)
        return jsonify(movies)
    except Exception as e:
        return jsonify({"error": f"Unable to fetch movies: {e}"}), 500


@api_bp.route('/vector_search', methods=['POST'])
def vector_search():
    try:
        data = request.json
        text = data.get('text')
        num_neighbors = data.get('num_neighbors', 5)

        if not text:
            return jsonify({"error": "Text is required"}), 400

        embedding = get_embedding(text)
        results = fetch_similar_movies(embedding, num_neighbors)
        return jsonify({"results": results, "query": text})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500


@api_bp.route('/generate', methods=['POST'])
def generate_prompt():
    try:
        # Extract prompt data from the request
        data = request.json
        prompt = data.get('prompt', "Why is the sky blue?")
        num_ctx = data.get('num_ctx', 512)

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
        
        system_prompt = "The system is a movie producer who crafts creative and engaging plots. \
            the system crates a plot summary meant to pitch to a director. The system uses the \
            terms provided by the user to create a plot summary in 25 tokens or less"

        # Send the request to the LLM service with streaming enabled
        response = requests.post(
            "http://llm:11434/api/chat",  # Use /api/chat instead of /api/generate
            json={
                "model": "llama3",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "The system is a movie producer who crafts creative and engaging plots. "
                            "The system creates a plot summary meant to pitch to a director. The system uses the "
                            "terms provided by the user to create a plot summary in 25 tokens or less. "
                            "No intro, just plain summary of the plot."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"{prompt}"
                    }
                ],
                "options": {
                    "num_ctx": 1024,  # Adjusted to model's max context size
                    "temperature": 1.2,
                    "num_predict": 25,  # 25 tokens to match "25 tokens or less" requirement
                    "top_k": 80,
                    "top_p": 0.9,
                    "min_p": 0.7
                }
            },
            headers={"Content-Type": "application/json"},
            stream=True  # If supported
        )


        if response.status_code != 200:
            return jsonify({"error": f"LLM service returned an error: {response.text}"}), response.status_code

        def generate():
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    yield chunk.decode('utf-8')  # Decode and forward each chunk

        return Response(generate(), content_type='application/json')
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500
