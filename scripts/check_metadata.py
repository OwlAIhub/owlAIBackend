import os
from pinecone import Pinecone

# Setup
api_key = os.getenv("PINECONE_API_KEY")
index_name = "ugc-net-data"

# Init Pinecone client
pc = Pinecone(api_key=api_key)

# Get index object
index = pc.Index(index_name)

# Dummy vector (make sure it matches your embedder dimension, e.g., 1536)
dummy_vector = [0.0] * 1536

# Query the index for any item
response = index.query(vector=dummy_vector, top_k=1, include_metadata=True)

# Print metadata (if available)
if response and response.get("matches"):
    metadata = response["matches"][0]["metadata"]
    print("✅ Metadata keys:", metadata.keys())
    print("🔎 Full metadata:", metadata)
else:
    print("❌ No matches found or metadata missing.")
