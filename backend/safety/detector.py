UNSAFE_KEYWORDS = [
    "pregnant", "pregnancy",
    "high blood pressure", "bp",
    "hernia", "glaucoma",
    "recent surgery"
]

def is_unsafe(query: str) -> bool:
    q = query.lower()
    return any(keyword in q for keyword in UNSAFE_KEYWORDS)
