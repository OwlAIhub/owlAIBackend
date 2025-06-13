from dotenv import load_dotenv
import os
from pinecone import Pinecone
from thefuzz import fuzz
from services.embedder import get_embedding

load_dotenv()

# Initialize Pinecone client
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))


def extract_topic_llm(query: str) -> list:
    from openai import OpenAI
    client = OpenAI()

    prompt = f"""
You are a smart assistant. Given a user query, extract the most relevant topic or title keyword (1–3 words max) that could match document titles.
Query: "{query}"
Return only the keyword or phrase, no explanations.
"""

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    raw = completion.choices[0].message.content.strip()
    return [t.strip().lower() for t in raw.split(",") if t.strip()]


def query_vector_store(query_text: str, top_k: int = 5, user_id: str = None):
    try:
        query_vector = get_embedding(query_text)
        topics = extract_topic_llm(query_text)
        print("Extracted Topic:", topics)

        # Step 1: Perform vector search (no Pinecone filter)
        res = index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True,
        )

        if res is None or not hasattr(res, "matches"):
            return []

        print("Retrieved Chunks Titles:")
        for i, match in enumerate(res.matches):
            title = match.metadata.get("title", "No title found")
            print(f"   [{i}] Title: {title}")
# Step 2: Fuzzy filter on both title and text
        filtered_matches = []
        for match in res.matches:
            title = match.metadata.get("title", "").lower()
            text = match.metadata.get("text", "").lower()

            for topic in topics:
                topic = topic.lower()
                title_score = fuzz.partial_ratio(topic, title)
                text_score = fuzz.partial_ratio(topic, text)

                print(f"Match check: Title '{title}' ~ Topic '{topic}' → {title_score}")
                print(f"Match check: Text ~ Topic '{topic}' → {text_score}")

                if max(title_score, text_score) > 60:
                    filtered_matches.append(match)
                    break


        # Step 3: Fallback if no good matches
        if not filtered_matches:
            print("No fuzzy title match. Returning top_k as fallback.")
            filtered_matches = res.matches[:top_k]

        # Step 4: Return final filtered content
        print(f"Final Chunks Sent to LLM: {len(filtered_matches)}")
        return [
            {"page_content": m.metadata.get("text", "")}
            for m in filtered_matches
            if "text" in m.metadata
        ]

    except Exception as e:
        print(f"[Pinecone Query Error] {str(e)}")
        return []
