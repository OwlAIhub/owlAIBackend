# app/services/vector_search.py

from dotenv import load_dotenv
import os
from pinecone import Pinecone
from services.embedder import get_embedding

load_dotenv()

# Initialize Pinecone client
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

def query_vector_store(query_text: str, top_k: int = 5, user_id: str = None):
    try:
        query_vector = get_embedding(query_text)

        filters = {}
        if user_id:
            filters["user_id"] = {"$eq": user_id}

        res = index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True,
            filter=filters if filters else None
        )

        if res is None or not hasattr(res, "matches"):
            return []

        return [match.metadata for match in res.matches if "text" in match.metadata]

    except Exception as e:
        # Optional: Log the error if you have logging setup
        print(f"[Pinecone Query Error] {str(e)}")
        return []
