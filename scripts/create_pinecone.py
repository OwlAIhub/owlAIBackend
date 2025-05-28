from dotenv import load_dotenv
load_dotenv()

import os
from pinecone import Pinecone, ServerlessSpec

# Load from environment
api_key = os.getenv("PINECONE_API_KEY")
env_region = os.getenv("PINECONE_ENVIRONMENT")  # e.g. "gcp-starter" → actually a region like "us-central1"

# Separate region and cloud from full env string
# Example: "gcp-starter" → cloud = "gcp", region = "us-central1"
cloud = "gcp"
region = env_region or "us-central1"

# Init Pinecone
pc = Pinecone(api_key=api_key)

index_name = "ugc-net-data"

# Check if index exists
existing = pc.list_indexes().names()
if index_name not in existing:
    pc.create_index(
        name=index_name,
        dimension=384,  # MiniLM
        metric="cosine",
        spec=ServerlessSpec(
            cloud=cloud,
            region=region
        )
    )
    print(f"Created index: {index_name}")
else:
    print(f"Index '{index_name}' already exists.")
