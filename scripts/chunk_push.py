import json, os, pinecone, hashlib
from uuid import uuid4
from tqdm import tqdm
from dotenv import load_dotenv
from openai import OpenAI

# === Load environment variables ===
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api = os.getenv("PINECONE_API_KEY")
pinecone_env = os.getenv("PINECONE_ENVIRONMENT")

# === Initialize Pinecone & OpenAI ===
pc = pinecone.Pinecone(api_key=pinecone_api)
index = pc.Index("ugc-net-data")

client = OpenAI(api_key=openai_api_key)

# === Embed using OpenAI ===
def embed(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# === Deterministic ID ===
def hash_id(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

# === Push each record ===
def push_chunk(title, summary, text):
    full_text = f"{title}\n\n{summary}\n\n{text}"
    embedding = embed(full_text)
    uid = hash_id(full_text)
    index.upsert([
        {
            "id": uid,
            "values": embedding,
            "metadata": {
                "title": title,
                "summary": summary,
                "text": text
            }
        }
    ])

# === Load your parsed JSON ===
with open("parsed_chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# === Upload to Pinecone ===
for i, chunk in tqdm(enumerate(chunks, 1), total=len(chunks), desc="🔼 Uploading"):
    title = chunk.get("title", "")
    summary = chunk.get("summary", "")
    text = chunk.get("text", "")
    push_chunk(title, summary, text)
