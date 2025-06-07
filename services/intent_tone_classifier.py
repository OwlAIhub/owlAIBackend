import os
import re
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def detect_language(query: str) -> str:
    hindi_chars = re.findall(r'[\u0900-\u097F]', query)
    english_chars = re.findall(r'[a-zA-Z]', query)
    hindi_words = ["hai", "kya", "nahi", "karna", "kyun", "tum", "mera", "batao", "shuru", "hona"]

    if len(hindi_chars) > 5:
        return "HINDI"
    elif any(w in query for w in hindi_words) and len(english_chars) > 3:
        return "HINGLISH"
    return "ENGLISH"

def detect_tone(query: str) -> str:
    if any(p in query for p in ["simple terms", "like a kid", "easy way"]):
        return "simple"
    if any(p in query for p in ["professor", "deep dive", "in detail"]):
        return "detailed"
    if any(p in query for p in ["i won't clear", "i can't", "i feel like giving up", "not doing well", "hopeless"]):
        return "emotional"
    if any(p in query for p in ["hi", "hello", "hey", "kaise ho", "namaste"]):
        return "casual"
    return "neutral"

def classify_intent_tone_language(query: str) -> dict:
    q = query.strip().lower()
    language = detect_language(q)
    tone = detect_tone(q)

    if q in ["a", "b", "c", "d"]:
        return {"intent": "quiz_answer", "tone": tone, "language": language}

    try:
        gpt_response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Classify the user query into ONE of the following intents:\n"
                        "- greeting: user says hello, hi, namaste\n"
                        "- academic: wants to learn a topic, asks for explanation\n"
                        "- quiz_start: wants a quiz to begin\n"
                        "- quiz_answer: answers a quiz question (A/B/C/D)\n"
                        "- quiz_continue: wants to resume a quiz\n"
                        "- quiz_review: wants to see score/review\n"
                        "- topic_list: asks for a list of points or subtopics\n"
                        "- emotional: feeling scared, unmotivated, sad\n"
                        "- source_query, privacy_query, creator_query: asks professional or ethical questions"
                    )
                },
                {"role": "user", "content": query}
            ],
            temperature=0
        )
        intent = gpt_response.choices[0].message.content.strip().lower()
    except Exception as e:
        print("GPT intent fallback error:", e)
        intent = "academic"

    return {
        "intent": intent,
        "tone": tone,
        "language": language
    }
