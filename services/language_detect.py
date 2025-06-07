import re

def detect_language_hint(query: str) -> str:
    query = query.lower()

    if "privacy" in query or "data" in query or "security" in query:
        return "Respond in clear, formal language with precise terminology."

    hindi = re.search(r'[\u0900-\u097F]', query)
    english = re.search(r'[a-zA-Z]', query)

    if hindi and english:
        return "HINGLISH"
    elif hindi:
        return "HINDI"
    else:
        return "ENGLISH"
