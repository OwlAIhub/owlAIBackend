from dotenv import load_dotenv
load_dotenv()

import os
from pinecone import Pinecone, ServerlessSpec

# Load from environment
api_key = os.getenv("PINECONE_API_KEY")
env_region = os.getenv("PINECONE_ENVIRONMENT")

cloud = "aws"
region = "us-east-1"

# Init Pinecone
pc = Pinecone(api_key=api_key)

index_name = "ugc-net-data"

# Check if index exists
existing = pc.list_indexes().names()
if index_name not in existing:
    pc.create_index(
        name=index_name,
        dimension=1536,  # ✅ OpenAI embeddings = 1536 dimensions
        metric="cosine",
        spec=ServerlessSpec(
            cloud=cloud,
            region=region
        )
    )
    print(f"✅ Created index: {index_name}")
else:
    print(f"⚠️ Index '{index_name}' already exists.")
