from flask import Blueprint, jsonify, request
from db import fetch_movies, fetch_similar_movies
from model_utils import get_embedding


api_bp = Blueprint('api', __name__, url_prefix='/')


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
        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500