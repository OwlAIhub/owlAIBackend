# services/intent_tone_classifier.py
import re

def classify_intent_tone_language(query: str) -> dict:
    q = query.strip().lower()

    # --- Language Detection ---
    hindi_chars = re.findall(r'[\u0900-\u097F]', q)
    english_chars = re.findall(r'[a-zA-Z]', q)
    hindi_words = ["hai", "kya", "nahi", "karna", "kyun", "tum", "mera", "batao", "shuru"]

    is_hindi_script = len(hindi_chars) > 5
    is_hinglish = any(word in q for word in hindi_words) and len(english_chars) > 3
    language = "HINDI" if is_hindi_script else "HINGLISH" if is_hinglish else "ENGLISH"

    # --- Tone Detection ---
    if any(t in q for t in ["simple terms", "like a kid", "easy way"]):
        tone = "simple"
    elif any(t in q for t in ["professor", "deep dive", "in detail"]):
        tone = "detailed"
    elif any(t in q for t in ["feeling low", "can't do this", "tired", "hopeless"]):
        tone = "emotional"
    elif any(t in q for t in ["hi", "hello", "namaste", "kaise ho"]):
        tone = "casual"
    else:
        tone = "neutral"

    # --- Intent Detection ---
    if any(p in q for p in ["source", "citation", "where did you learn"]):
        intent = "source_query"
    elif any(p in q for p in ["privacy", "data policy", "who can read"]):
        intent = "privacy_query"
    elif any(p in q for p in ["creator", "who made you", "developer"]):
        intent = "creator_query"
    elif any(p in q for p in ["quiz", "test me", "practice question", "ask me question"]):
        intent = "quiz_start"
    elif any(p in q for p in ["next question", "continue quiz", "resume quiz"]):
        intent = "quiz_continue"
    elif q.strip().upper() in ["A", "B", "C", "D"]:
        intent = "quiz_answer"
    elif any(p in q for p in ["review", "how did i do", "my score"]):
        intent = "quiz_review"
    elif any(p in q for p in ["repeat", "again", "say that again", "rephrase"]):
        intent = "rephrase"
    elif any(p in q for p in ["hi", "hello", "hey", "kaise ho"]):
        intent = "greeting"
    elif any(p in q for p in ["motivate", "inspire", "burnt out"]):
        intent = "motivational"
    else:
        intent = "academic"

    return {
        "intent": intent,
        "tone": tone,
        "language": language
    }
