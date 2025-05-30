import json, os, pinecone, hashlib
from uuid import uuid4
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Pinecone init
pinecone_api = os.getenv("PINECONE_API_KEY")
pinecone_env = os.getenv("PINECONE_ENVIRONMENT")
pc = pinecone.Pinecone(api_key=pinecone_api)
index = pc.Index("ugc-net-data")

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 🔐 Deterministic ID for deduplication
def hash_id(text: str) -> str:
    return hashlib.md5(text.encode('utf-8')).hexdigest()

# 📦 Smart chunker
def smart_chunk(text, max_words=300):
    sentences = text.split(". ")
    chunks, chunk = [], ""
    for s in sentences:
        if len((chunk + s).split()) > max_words:
            chunks.append(chunk.strip())
            chunk = s + ". "
        else:
            chunk += s + ". "
    if chunk.strip():
        chunks.append(chunk.strip())
    return chunks

# 🔁 Embed & push
def embed(text): return model.encode(text).tolist()

def push(chunks, metadata):
    for chunk in chunks:
        index.upsert([
            {
                "id": hash_id(chunk),
                "values": embed(chunk),
                "metadata": {
                    **metadata,
                    "text": chunk
                }
            }
        ])

# 📄 Load JSON
with open("../UGC_NET_Paper1_Combined_Firestore_Format.json", "r", encoding="utf-8") as f:
    data = json.load(f)

ugcnet_data = data["UGC NET"]["Paper 1"]

# 📘 Book Content
for subject, topics in tqdm(ugcnet_data["Book Content"].items(), desc="📘 Book Content"):
    for topic, content in topics.items():
        if isinstance(content, str) and content.strip():
            push(smart_chunk(content), {
                "source": "book_content", "subject": subject, "topic": topic
            })
        elif isinstance(content, dict):
            for subtopic, subcontent in content.items():
                if isinstance(subcontent, str) and subcontent.strip():
                    push(smart_chunk(subcontent), {
                        "source": "book_content",
                        "subject": subject,
                        "topic": topic,
                        "subtopic": subtopic
                    })

# 📒 Syllabus
for unit, topics in tqdm(ugcnet_data["Syllabus"].items(), desc="📒 Syllabus"):
    for topic in topics:
        if topic.strip():
            push(smart_chunk(topic), {
                "source": "syllabus", "unit": unit, "topic": topic
            })

# 📝 PYQs
for year, sets in tqdm(ugcnet_data["PYQs"].items(), desc="📝 PYQs"):
    if isinstance(sets, list):
        # No set structure, just list of questions
        for q in sets:
            if isinstance(q, dict) and "question" in q and "options" in q and "answer" in q:
                full = f"Q: {q['question']}\nOptions: {', '.join(q['options'])}\nAnswer: {q['answer']}"
                push(smart_chunk(full), {
                    "source": "pyq", "year": year
                })
    elif isinstance(sets, dict):
        # Sets like "Set 1", "Set 2"
        for set_name, questions in sets.items():
            for q in questions:
                if isinstance(q, dict) and "question" in q and "options" in q and "answer" in q:
                    full = f"Q: {q['question']}\nOptions: {', '.join(q['options'])}\nAnswer: {q['answer']}"
                    push(smart_chunk(full), {
                        "source": "pyq", "year": year, "set": set_name
                    })
