import psycopg2
from psycopg2.extras import RealDictCursor
from model_utils import normalize_query_embedding, format_vector_for_postgres
from logger import logger

# Database connection settings
DB_CONFIG = {
    "dbname": "movie_recco",
    "user": "user",
    "password": "password",
    "host": "db",
    "port": 5432,
}

def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise

def fetch_movies(limit=10, title_filter="", offset=0):
    """Fetch movies with optional fuzzy title matching and pagination."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
            conn.commit()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = """
                SELECT 
                    id,
                    title,
                    release_year,
                    director,
                    origin_ethnicity,
                    plot_summary,
                    genre,
                    "cast"
                FROM movies
                WHERE 
                    CASE 
                        WHEN %s != '' THEN 
                            title ILIKE %s
                            OR similarity(lower(title), lower(%s)) > 0.3
                        ELSE TRUE
                    END
                ORDER BY 
                    CASE 
                        WHEN %s != '' THEN similarity(lower(title), lower(%s))
                        ELSE release_year 
                    END DESC
                OFFSET %s
                LIMIT %s;
            """
            like_pattern = f"%{title_filter}%" if title_filter else ""
            cursor.execute(
                query,
                (title_filter, like_pattern, title_filter, title_filter, title_filter, offset, limit)
            )
            return cursor.fetchall() 
    except Exception as e:
        print(f"Error fetching movies: {e}")
        raise
    finally:
        conn.close()

def fetch_similar_movies(embedding, num_neighbors=5, metric='cosine'):
    conn = get_db_connection()
    try:
        if metric == 'cosine':
            embedding = normalize_query_embedding(embedding)
            embedding_column = "embedding_normalized"
            similarity_calc = f"1 - ({embedding_column} <=> %s::vector)"
        elif metric == 'euclidean':
            embedding_column = "embedding_original"
            similarity_calc = f"-({embedding_column} <-> %s::vector)"
        else:
            raise ValueError("Metric must be either 'cosine' or 'euclidean'")
        query = f"""
            SELECT 
                title,
                release_year,
                plot_summary,
                director,
                origin_ethnicity,
                genre,
                "cast",
                {similarity_calc} as similarity
            FROM movies
            WHERE {embedding_column} IS NOT NULL
            ORDER BY similarity asc
            LIMIT %s;
        """
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, [embedding.tolist(), num_neighbors])
            return cursor.fetchall()
    finally:
        conn.close()

def search_movies_hybrid(embedding, text_query="", num_neighbors=5, metric='cosine', 
                        use_normalized=True, embedding_weight=0.7, min_similarity=0.0):
    """Search movies using both embedding similarity and text matching."""
    if not 0 <= embedding_weight <= 1:
        raise ValueError("embedding_weight must be between 0 and 1")
    conn = get_db_connection()
    try:
        embedding_to_use = normalize_query_embedding(embedding) if metric == 'cosine' else embedding
        pg_vector = format_vector_for_postgres(embedding_to_use)
        embedding_column = "embedding_normalized" if use_normalized else "embedding_original"
        if metric == 'cosine':
            similarity_calc = f"1 - ({embedding_column} <=> '{pg_vector}'::vector)"
        else:
            similarity_calc = f"exp(-0.1 * ({embedding_column} <-> '{pg_vector}'::vector))"
        text_match = """
            to_tsvector('english', coalesce(title, '') || ' ' || coalesce(plot_summary, ''))
        """
        query = f"""
            WITH similarity_scores AS (
                SELECT 
                    *,
                    {similarity_calc} as embedding_similarity,
                    CASE 
                        WHEN %s != '' THEN 
                            ts_rank_cd(
                                {text_match},
                                plainto_tsquery('english', %s)
                            )
                        ELSE 0
                    END as text_similarity
                FROM movies
                WHERE {embedding_column} IS NOT NULL
                AND CASE 
                    WHEN %s != '' THEN 
                        {text_match} @@ plainto_tsquery('english', %s)
                    ELSE TRUE
                END
            )
            SELECT 
                title,
                release_year,
                plot_summary,
                director,
                origin_ethnicity,
                genre,
                "cast",
                embedding_similarity,
                text_similarity,
                (%s * embedding_similarity + (1 - %s) * NULLIF(text_similarity, 0)) as combined_similarity
            FROM similarity_scores
            WHERE (%s * embedding_similarity + (1 - %s) * NULLIF(text_similarity, 0)) >= %s
            ORDER BY combined_similarity DESC NULLS LAST
            LIMIT %s;
        """
        params = [
            text_query,                # For CASE WHEN check
            text_query,                # For plainto_tsquery in ts_rank_cd
            text_query,                # For CASE WHEN in WHERE clause
            text_query,                # For plainto_tsquery in WHERE clause
            embedding_weight,          # For similarity calculation
            embedding_weight,          # For similarity calculation (1 - weight)
            embedding_weight,          # For WHERE clause
            embedding_weight,          # For WHERE clause (1 - weight)
            min_similarity,            # For minimum similarity threshold
            num_neighbors             # For LIMIT
        ]
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    except Exception as e:
        print(f"Error in hybrid search: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    example_embedding = [0.1, 0.2, 0.3, 0.4]  # truncated for brevity
    
    # Basic queries
    movies = fetch_movies(limit=10)
    star_movies = fetch_movies(title_filter="star", limit=5)
    next_page = fetch_movies(title_filter="star", limit=5, offset=5)
    
    # Similarity searches
    cosine_results = fetch_similar_movies(embedding=example_embedding, metric='cosine')
    euclidean_results = fetch_similar_movies(embedding=example_embedding, metric='euclidean')
    
    # Hybrid search
    hybrid_results = search_movies_hybrid(
        embedding=example_embedding,
        text_query="action adventure",
        embedding_weight=0.7
    )