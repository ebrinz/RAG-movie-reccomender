import psycopg2
from psycopg2.extras import execute_values
import json
import os

# Connect to PostgreSQL
conn = psycopg2.connect("dbname='movie_recco' user='user' password='password' host='localhost'")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS movies;")

# Create table
cur.execute("""
CREATE TABLE IF NOT EXISTS movies (
    release_year INTEGER,
    title TEXT,
    origin_ethnicity TEXT,
    director TEXT,
    "cast" TEXT,
    genre TEXT,
    wiki_page TEXT,
    plot TEXT,
    plot_summary TEXT,
    embedding DOUBLE PRECISION[]
);
""")
conn.commit()

# Ingest data from chunks
chunk_dir = "./data/chunks"
chunk_files = [os.path.join(chunk_dir, f) for f in os.listdir(chunk_dir) if f.endswith(".json")]

for chunk_file in sorted(chunk_files):
    print(f"Ingesting data from {chunk_file}...")
    with open(chunk_file, "r") as f:
        rows = []
        for line in f:
            record = json.loads(line)
            rows.append((
                record.get('Release Year'),
                record.get('Title'),
                record.get('Origin/Ethnicity'),
                record.get('Director'),
                record.get('Cast'),
                record.get('Genre'),
                record.get('Wiki Page'),
                record.get('Plot'),
                record.get('PlotSummary'),
                record.get('embedding')
            ))

        execute_values(
            cur,
            """
            INSERT INTO movies (
                release_year, title, origin_ethnicity, director, "cast", genre, 
                wiki_page, plot, plot_summary, embedding
            ) VALUES %s
            """,
            rows
        )
    conn.commit()

cur.close()
conn.close()
print("Data successfully ingested into PostgreSQL!")
