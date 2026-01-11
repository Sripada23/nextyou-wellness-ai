from sentence_transformers import SentenceTransformer

# Load model ONCE at startup (important)
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts):
    return model.encode(texts)
