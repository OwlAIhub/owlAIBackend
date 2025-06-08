# services/intent_tone_classifier.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-3.5-turbo"  # You can use gpt-3.5-turbo if needed

def classify_intent_tone_language(query: str) -> dict:
    query = query.strip()

    try:
        prompt = [
            {"role": "system", "content": (
                "You are a smart classifier for a UGC NET teaching assistant bot called OwlAI.\n"
                "Classify the following query into:\n"
                "- intent: one of [greeting, syllabus_query, concept_explanation, chapter_teaching, quiz_start, quiz_answer, quiz_continue, motivational, emotional, review_request, rephrase, professional_query]\n"
                "- tone: one of [casual, detailed, simple, emotional, neutral, motivational, kid-style]\n"
                "- language: one of [ENGLISH, HINDI, HINGLISH]\n\n"
                "Respond only in JSON like this:\n"
                '{"intent": "concept_explanation", "tone": "simple", "language": "HINGLISH"}'
            )},
            {"role": "user", "content": f"Query: {query}"}
        ]

        response = client.chat.completions.create(
            model=MODEL,
            messages=prompt,
            temperature=0
        )

        result = response.choices[0].message.content.strip()
        return eval(result) if result.startswith("{") else {
            "intent": "concept_explanation",
            "tone": "neutral",
            "language": "ENGLISH"
        }

    except Exception as e:
        print("[Classification Error]", e)
        return {
            "intent": "concept_explanation",
            "tone": "neutral",
            "language": "ENGLISH"
        }
