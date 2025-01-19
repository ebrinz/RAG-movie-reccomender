import os
from dotenv import load_dotenv
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, ModernBertModel, ModernBertConfig


def load_model():
    model_name = os.getenv("EMBEDDING_MODEL")
    if "modernbert" in model_name.lower():
        config = ModernBertConfig()
        tokenizer = AutoTokenizer.from_pretrained(model_name);
        model = ModernBertModel.from_pretrained(model_name, trust_remote_code=True)
    else:
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        model = AutoModelForSequenceClassification.from_pretrained(model_name, trust_remote_code=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()
    return tokenizer, model, device

def get_embedding(text, tokenizer, model, device):  
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    inputs = {key: val.to(device) for key, val in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)
    last_hidden_state = outputs.hidden_states[-1]
    cls_embedding = last_hidden_state[0, 0, :]
    return cls_embedding.cpu().numpy().tolist()


if __name__ == "__main__":
    tokenizer, model, device = load_model()
    text = "The wheel in the sky keeps on turning."
    embedding = get_embedding(text, tokenizer, model, device)
    print("Generated embedding:", embedding)