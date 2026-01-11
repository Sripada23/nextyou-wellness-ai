from fastapi import FastAPI

from backend.rag.loader import load_documents
from backend.rag.retriever import Retriever
from backend.safety.detector import is_unsafe
from backend.db.mongo import log_query


app = FastAPI(title="Ask Me Anything About Yoga")

documents = load_documents()
retriever = Retriever(documents)

@app.post("/ask")
def ask(query: str):
    unsafe = is_unsafe(query)
    sources = retriever.retrieve(query)

    if unsafe:
        answer = (
            "⚠️ This question involves health-related risks. "
            "Please consult a certified yoga instructor or medical professional."
        )
    else:
        context = " ".join([s["text"] for s in sources])
        answer = f"Based on yoga knowledge: {context}"

    log_query({
        "query": query,
        "sources": sources,
        "answer": answer,
        "isUnsafe": unsafe
    })

    return {
        "answer": answer,
        "sources": [{"id": s["id"], "title": s["title"]} for s in sources],
        "isUnsafe": unsafe
    }
