from pymongo import MongoClient
from datetime import datetime

def log_query(entry: dict):
    try:
        client = MongoClient(
            "mongodb://localhost:27017",
            serverSelectionTimeoutMS=2000
        )
        db = client["nextyou_rag"]
        entry["timestamp"] = datetime.utcnow()
        db.logs.insert_one(entry)
    except Exception as e:
        # Safe fallback: app should NOT crash if MongoDB is unavailable
        print("MongoDB not available, skipping log.")
