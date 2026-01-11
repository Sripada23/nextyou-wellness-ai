import faiss
import numpy as np
from .embedder import embed_texts

class Retriever:
    def __init__(self, documents):
        self.documents = documents
        texts = [doc["text"] for doc in documents]
        embeddings = embed_texts(texts)

        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(np.array(embeddings))

    def retrieve(self, query, k=3):
        query_embedding = embed_texts([query])
        _, indices = self.index.search(np.array(query_embedding), k)
        return [self.documents[i] for i in indices[0]]
