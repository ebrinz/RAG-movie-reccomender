import os
import pandas as pd
import numpy as np
from tqdm.auto import tqdm
from concurrent.futures import ThreadPoolExecutor
import psycopg2
from psycopg2.extras import execute_values
import json

def load_all_records(chunk_files):
    all_records = []
    for chunk_file in tqdm(sorted(chunk_files), desc="Loading chunks"):
        with open(chunk_file, "r") as f:
            for line in f:
                record = json.loads(line)
                if record.get('embedding') is not None:
                    all_records.append(record)
    return all_records

def ingest():
    vector_length = os.getenv("VECTOR_LENGTH", "768")
    conn = psycopg2.connect("dbname='movie_recco' user='user' password='password' host='db'")
    cur = conn.cursor()
    
    cur.execute("DROP TABLE IF EXISTS movies;")
    cur.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    cur.execute(f"""
    CREATE TABLE movies (
        id SERIAL PRIMARY KEY,
        release_year INTEGER,
        title TEXT NOT NULL,
        origin_ethnicity TEXT,
        director TEXT,
        "cast" TEXT,
        genre TEXT,
        wiki_page TEXT,
        plot TEXT,
        plot_summary TEXT,
        embedding_original vector({vector_length}),
        embedding_normalized vector({vector_length})
    );
    """)
    
    cur.execute("""
    CREATE INDEX idx_embedding_original ON movies USING ivfflat (embedding_original) WITH (lists = 100);
    """)
    cur.execute("""
    CREATE INDEX idx_embedding_normalized ON movies USING ivfflat (embedding_normalized) WITH (lists = 100);
    """)
    cur.execute("""
    CREATE INDEX idx_title ON movies (title);
    """)
    
    # Load and process chunks
    chunk_dir = "./data/chunks"
    chunk_files = [os.path.join(chunk_dir, f) for f in os.listdir(chunk_dir) if f.endswith(".json")]
    
    # Load all records first
    print("Loading all records to process embeddings...")
    all_records = load_all_records(chunk_files)
    
    print("Loading and normalizing embeddings...")
    all_embeddings = np.stack([np.array(r['embedding']) for r in all_records])
    l2_norms = np.sqrt(np.sum(all_embeddings ** 2, axis=1, keepdims=True))
    normalized_embeddings = all_embeddings / l2_norms
    
    print("Preparing records for bulk insert...")
    rows = [
        (
            record.get('Release Year'),
            record.get('Title'),
            record.get('Origin/Ethnicity'),
            record.get('Director'),
            record.get('Cast'),
            record.get('Genre'),
            record.get('Wiki Page'),
            record.get('Plot'),
            record.get('PlotSummary'),
            all_embeddings[i].tolist(),
            normalized_embeddings[i].tolist()
        )
        for i, record in enumerate(all_records)
    ]
    
    execute_values(
        cur,
        """
        INSERT INTO movies (
            release_year, title, origin_ethnicity, director, "cast", genre, 
            wiki_page, plot, plot_summary, embedding_original, embedding_normalized
        ) VALUES %s
        """,
        rows,
        page_size=1000
    )
    conn.commit()
    
    cur.close()
    conn.close()
    print("Data successfully ingested into PostgreSQL with both original and normalized embeddings!")

if __name__ == "__main__":
    ingest()
    print("Data ingestion completed.")