import os
import pandas as pd
from tqdm.auto import tqdm
from concurrent.futures import ThreadPoolExecutor
from model_utils import load_model, get_embedding
import psycopg2
from psycopg2.extras import execute_values
import json


# Function to process a chunk of data
def process_chunk(chunk, output_file, tokenizer, model, device):
    chunk["embedding"] = chunk["PlotSummary"].progress_apply(lambda text: get_embedding(text, tokenizer, model, device))
    chunk.to_json(output_file, orient="records", lines=True)
    print(f"Processed and saved chunk to {output_file}")

# Check if chunk file already exists and is complete
def is_chunk_complete(output_file, expected_count):
    if not os.path.exists(output_file):
        return False
    with open(output_file, "r") as f:
        count = sum(1 for _ in f)
    return count == expected_count

# Main function
def generate(tokenizer, model, device):
    tqdm.pandas()
    url = "https://huggingface.co/datasets/vishnupriyavr/wiki-movie-plots-with-summaries/resolve/main/wiki_movie_plots_deduped_with_summaries.csv"
    try:
        movie_df = pd.read_csv(url)
        print("DataFrame loaded successfully!")
    except Exception as e:
        print(f"An error occurred while loading the CSV: {e}")
        return
    
    # filter out some stuff here for expedience and relevance
    movie_df = movie_df[
        (movie_df['Origin/Ethnicity'] == 'American') &
        (movie_df['Release Year'] >= 1950)
    ]
    movie_df["Plot"] = movie_df["Plot"].astype(str)
    movie_df["PlotSummary"] = movie_df["PlotSummary"].astype(str)

    ####### FOR TEST ONLY!!!!######
    # movie_df = movie_df.head(50)
    ###############################

    chunk_size = 1000
    num_chunks = len(movie_df) // chunk_size + int(len(movie_df) % chunk_size > 0)
    chunks = [movie_df.iloc[i * chunk_size:(i + 1) * chunk_size] for i in range(num_chunks)]

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for idx, chunk in enumerate(chunks):
            output_file = f"./data/chunks/movie_embeddings_chunk_{idx + 1}.json"
            if not is_chunk_complete(output_file, len(chunk)):
                futures.append(executor.submit(process_chunk, chunk, output_file, tokenizer, model, device))
        for future in tqdm(futures, desc="Processing Chunks"):
            future.result()


if __name__ == "__main__":
    tokenizer, model, device = load_model()
    print("Getting data.")
    generate(tokenizer, model, device)







    