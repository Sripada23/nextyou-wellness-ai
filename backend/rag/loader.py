import json

def load_documents(path="data/yoga_articles.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
