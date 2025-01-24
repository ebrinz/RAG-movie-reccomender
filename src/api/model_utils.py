import os
from dotenv import load_dotenv
import torch
import numpy as np
import argparse
from transformers import AutoTokenizer, AutoModelForSequenceClassification, ModernBertModel, ModernBertConfig
from typing import List


# refactor logging
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ]
)

def format_vector_for_postgres(embedding):
    return f"[{','.join(map(str, embedding))}]"

def load_model():
    model_name = os.getenv("EMBEDDING_MODEL")
    ##### test
    # if "modernbert" in model_name.lower():
    #     config = ModernBertConfig()
    #     tokenizer = AutoTokenizer.from_pretrained(model_name);
    #     model = ModernBertModel.from_pretrained(model_name, trust_remote_code=True)
    # else:
    #     exit #### test
    #     tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    #     model = AutoModelForSequenceClassification.from_pretrained(model_name, trust_remote_code=True)
    config = ModernBertConfig()
    tokenizer = AutoTokenizer.from_pretrained(model_name);
    model = ModernBertModel.from_pretrained(model_name, trust_remote_code=True)
    #######
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()
    return tokenizer, model, device

def get_embedding(text: str, tokenizer, model, device):
    try:
        inputs = tokenizer(
            text,
            add_special_tokens=True,
            max_length=512,
            padding=True,
            truncation=True,
            return_tensors='pt'
        ).to(device)
        
        with torch.no_grad():
            outputs = model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)

        embedding = embeddings[0].cpu().numpy()
        if embedding.size == 0:
            raise ValueError("Generated embedding is empty")
        return embedding
        
    except Exception as e:
        logging.error(f"Error in get_embedding: {str(e)}", exc_info=True)
        raise

def normalize_query_embedding(embedding):
    if embedding is None:
        raise ValueError("Embedding cannot be None")
    return embedding / np.linalg.norm(embedding)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate embeddings for a given text.")
    parser.add_argument(
        "--text",
        type=str,
        required=True,
        help="The text for which to generate an embedding."
    )
    args = parser.parse_args()
    tokenizer, model, device = load_model()
    embedding = get_embedding(args.text, tokenizer, model, device)
    print("Generated embedding:", embedding)