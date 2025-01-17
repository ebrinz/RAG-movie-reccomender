import torch
import pandas as pd
from tqdm.auto import tqdm
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from concurrent.futures import ThreadPoolExecutor
import os
import json

tqdm.pandas()

# Load model and tokenizer
model_name = "answerdotai/ModernBERT-large"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForSequenceClassification.from_pretrained(model_name, trust_remote_code=True)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

# Function to get embedding
def get_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    inputs = {key: val.to(device) for key, val in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)
    last_hidden_state = outputs.hidden_states[-1]
    cls_embedding = last_hidden_state[0, 0, :]
    return cls_embedding.cpu().numpy().tolist()

# Function to process a chunk of data
def process_chunk(chunk, output_file):
    chunk["embedding"] = chunk["Plot"].progress_apply(get_embedding)
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
def main():
    url = "https://huggingface.co/datasets/vishnupriyavr/wiki-movie-plots-with-summaries/resolve/main/wiki_movie_plots_deduped_with_summaries.csv"

    try:
        movie_df = pd.read_csv(url)
        print("DataFrame loaded successfully!")
    except Exception as e:
        print(f"An error occurred while loading the CSV: {e}")
        return

    movie_df["Plot"] = movie_df["Plot"].astype(str)

    chunk_size = 1000
    num_chunks = len(movie_df) // chunk_size + int(len(movie_df) % chunk_size > 0)
    chunks = [movie_df.iloc[i * chunk_size:(i + 1) * chunk_size] for i in range(num_chunks)]

    os.makedirs("./chunks", exist_ok=True)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for idx, chunk in enumerate(chunks):
            output_file = f"./data/chunks/movie_embeddings_chunk_{idx + 1}.json"
            if not is_chunk_complete(output_file, len(chunk)):
                futures.append(executor.submit(process_chunk, chunk, output_file))
        for future in tqdm(futures, desc="Processing Chunks"):
            future.result()

if __name__ == "__main__":
    main()
