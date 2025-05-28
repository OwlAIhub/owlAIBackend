# app/services/vector_search.py

from dotenv import load_dotenv
import os
from pinecone import Pinecone
from services.embedder import get_embedding

load_dotenv()

# Initialize Pinecone client
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Load Pinecone index
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

def query_vector_store(query_text: str, top_k: int = 5):
    # Get embedding for query
    query_vector = get_embedding(query_text)

    # Perform similarity search
    res = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True
    )

    # Extract context text from metadata
    documents = []
    for match in res.matches:
        if match.metadata and "text" in match.metadata:
            documents.append(match.metadata["text"])

    return documents
