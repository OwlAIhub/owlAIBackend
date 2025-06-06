# ✅ Updated intent_classifier.py
# Clean and structured intent classifier with tone awareness

def classify_intent(query: str) -> str:
    query = query.lower().strip()

    # 🔹 Professional/system queries
    if any(p in query for p in ["source", "citation", "reference", "where did you learn"]):
        return "source_query"
    if any(p in query for p in ["privacy", "data policy", "gdpr", "who can read", "is my data"]):
        return "privacy_query"
    if any(p in query for p in ["who made you", "creator", "developer", "openai"]):
        return "creator_query"

    # 🔹 Meta
    if any(word in query for word in ["chatgpt", "which model", "are you gpt", "ai model"]):
        return "meta"

    # 🔹 Academic signals
    academic_phrases = ["explain", "define", "ugc net", "syllabus", "teaching aptitude", "research methodology"]
    if any(word in query for word in academic_phrases):
        return "academic"

    # 🔹 MCQ and quiz
    if any(word in query for word in ["mcq", "quiz", "test me", "practice question", "ask me question"]):
        return "mcq"

    # 🔹 Feedback about user
    if any(word in query for word in ["how prepared", "rate me", "how am i doing", "progress"]):
        return "feedback"

    # 🔹 Motivation
    if any(word in query for word in ["motivate", "inspire", "feeling low", "why should i study"]):
        return "motivational"

    # 🔹 Casual greetings
    if any(word in query for word in ["hello", "hi", "hey", "what's up", "kaise ho", "namaste"]):
        return "casual"

    # 🔹 Off-topic
    if any(word in query for word in ["cricket", "movie", "joke", "music", "weather", "news"]):
        return "off_topic"

    # 🔹 Emotional support
    if any(word in query for word in ["stressed", "anxious", "burnt out", "i'm tired", "can't do this"]):
        return "emotional"

    # 🔹 Tone modifiers
    if any(tone in query for tone in ["like a kid", "in simple terms", "explain like"]):
        return "tone_simple"
    if any(tone in query for tone in ["like a professor", "in detail", "deep dive"]):
        return "tone_detailed"

    # 🔹 Default fallback
    return "academic"
