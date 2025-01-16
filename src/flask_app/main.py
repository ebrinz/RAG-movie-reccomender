from flask import Flask, Blueprint, jsonify

api_bp = Blueprint('api', __name__, url_prefix='/api')

# import psycopg2

# def get_connection():
#     return psycopg2.connect(
#         dbname='movie_recco',
#         user='user',
#         password='password',
#         host='postgres'  # Use the service name from docker-compose for internal connectivity
#     )
# def fetch_movies(limit):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM movies LIMIT %s", (limit,))
#     results = cur.fetchall()
#     cur.close()
#     conn.close()
#     return results

# def fetch_movies_by_year(year):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM movies WHERE release_year = %s", (year,))
#     results = cur.fetchall()
#     cur.close()
#     conn.close()
#     return results

# def search_movies_by_title(substring):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM movies WHERE title ILIKE %s", (f"%{substring}%",))
#     results = cur.fetchall()
#     cur.close()
#     conn.close()
#     return results

# def fetch_movie_embeddings(movie_title):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT embedding FROM movies WHERE title = %s", (movie_title,))
#     result = cur.fetchone()
#     cur.close()
#     conn.close()
#     return result


@api_bp.route('/process', methods=['GET'])
def process_data():
    return jsonify({"message": "Processing data!"})

app = Flask(__name__)
@app.route('/')
def home():
    return "Hello, Flask!"
app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)