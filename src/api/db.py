import psycopg2
from psycopg2.extras import RealDictCursor
import numpy as np

# Database connection settings
DB_CONFIG = {
    "dbname": "movie_recco",
    "user": "user",
    "password": "password",
    "host": "postgres",
    "port": 5432,
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise

def fetch_movies(limit=10, title_filter=""):
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = """
                SELECT * FROM movies
                LIMIT 5;
            """
            like_pattern = f"{title_filter}%"
            cursor.execute(query, (like_pattern, limit))
            movies = cursor.fetchall()
        return movies
    finally:
        conn.close()

def fetch_similar_movies(embedding, num_neighbors=5):
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = """
                SELECT title, release_year, plot, director, origin_ethnicity,
                       embedding <-> %s AS similarity
                FROM movies
                ORDER BY similarity ASC
                LIMIT %s;
            """
            cursor.execute(query, (embedding, num_neighbors))
            results = cursor.fetchall()
        return results
    finally:
        conn.close()
