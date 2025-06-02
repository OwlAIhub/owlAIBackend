def classify_intent(query: str) -> str:
    query = query.lower()

    if any(word in query for word in ["motivate", "why should i", "benefit of ugc net"]):
        return "motivational"
    elif any(word in query for word in ["mcq", "quiz", "give me questions", "ask me questions"]):
        return "mcq"
    elif any(word in query for word in ["rate me", "how prepared", "percentage"]):
        return "feedback"
    elif any(word in query for word in ["who created", "are you chatgpt", "what model", "openai"]):
        return "meta"
    elif any(word in query for word in ["joke", "news", "cricket", "weather"]):
        return "off_topic"
    elif any(word in query for word in ["feel like giving up", "hopeless", "stressed"]):
        return "emotional"

    return "academic"
