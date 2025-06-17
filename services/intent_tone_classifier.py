import os
import re
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-3.5-turbo"

# Basic topic extractor as fallback
def extract_topic(query: str) -> str:
    match = re.search(r"(?:quiz|test|teach|explain|on)\s*(?:on|about)?\s*(.+)", query.lower())
    if match:
        return match.group(1).strip()
    return "UGC NET"

def classify_intent_language_topic(query: str) -> dict:
    query = query.strip()

    # Fast-track check for quiz options
    if query.upper() in ["A", "B", "C", "D"]:
        return {
            "intent": "quiz_answer",
            "language": "ENGLISH",
            "topic": "UGC NET"
        }

    prompt = [
        {"role": "system", "content": (
            "You're a smart classifier helping a UGC NET tutor bot.\n"
            "You must read the student's message and classify it into the following JSON structure:\n\n"
            '{\n'
            '  "intent": "greeting | concept_explanation | chapter_teaching | quiz_request | quiz_answer | syllabus_query | emotion | off-topic",\n'
            '  "language": "ENGLISH | HINDI | HINGLISH",\n'
            '  "topic": "subject or chapter name like Teaching Aptitude"\n'
            '}\n\n'
            "Guidelines:\n"
            "- Use 'HINGLISH' if the query mixes English and casual Hindi.\n"
            "- Use 'HINDI' only if the query is in pure Hindi (without English words).\n"
            "- Don't use formal or complex Hindi like 'uddheshyapurn', etc.\n"
            "- Only return valid JSON. No comments, no explanation."
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
            "language": "HINGLISH" if any(h in query.lower() for h in ["kya", "kaise", "hai", "nahi", "padhao", "samjhao"]) else "ENGLISH",
            "topic": extract_topic(query)
        }
