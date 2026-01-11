import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient

# Load .env from project root safely
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(dotenv_path=BASE_DIR / ".env")

MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI not found in environment variables")

client = MongoClient(MONGODB_URI)
db = client["nextyou_wellness_rag"]
logs_collection = db["logs"]

def log_query(entry: dict):
    try:
        logs_collection.insert_one(entry)
        print("✅ Logged to MongoDB Atlas")
    except Exception as e:
        print("❌ MongoDB log failed:", e)
