import os
import re
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-3.5-turbo"

# Extract just the topic (fallback if classification fails)
def extract_topic(query: str) -> str:
    match = re.search(r"(?:quiz|test|teach|explain|on)\s*(?:on|about)?\s*(.+)", query.lower())
    if match:
        return match.group(1).strip()
    return "UGC NET"

# SIMPLIFIED CLASSIFIER
def classify_intent_language_topic(query: str) -> dict:
    query = query.strip()

    # Shortcut for quiz answer
    if query.upper() in ["A", "B", "C", "D"]:
        return {
            "intent": "quiz_answer",
            "language": "ENGLISH",
            "topic": "UGC NET"
        }

    prompt = [
        {"role": "system", "content": (
            "You are a smart classifier for an AI UGC NET tutor.\n"
            "Classify the query into this JSON format:\n\n"
            '{\n'
            '  "intent": "greeting | concept_explanation | chapter_teaching | quiz_request | quiz_answer | syllabus_query | emotion | off-topic",\n'
            '  "language": "ENGLISH | HINDI | HINGLISH",\n'
            '  "topic": "subject or chapter name like Teaching Aptitude"\n'
            '}\n\n'
            "Only return valid JSON. No explanations."
        )},
        {"role": "user", "content": f"Query: {query}"}
    ]

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=prompt,
            temperature=0
        )
        return json.loads(response.choices[0].message.content.strip())

    except Exception as e:
        print("[Classification Error]", e)
        return {
            "intent": "concept_explanation",
            "language": "ENGLISH",
            "topic": extract_topic(query)
        }
