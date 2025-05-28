# services/llm.py

import os
from dotenv import load_dotenv
load_dotenv()  # ✅ load .env first

# ⛔ important: force set credentials path early
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

import vertexai
from vertexai.language_models import TextGenerationModel

project = os.getenv("VERTEX_PROJECT_ID")
location = os.getenv("VERTEX_LOCATION")

# ✅ Initialize Vertex with project + region
vertexai.init(project=project, location=location)

model = TextGenerationModel.from_pretrained("text-bison")

def build_prompt(query: str, context_chunks: list) -> str:
    context = "\n\n".join([c['metadata']['text'] for c in context_chunks])
    return (
        f"You are OwlAI, a friendly tutor for UGC NET Paper 1.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n"
        f"Answer in short, clear bullet points with examples."
    )

def get_response_from_llm(prompt: str) -> str:
    response = model.predict(prompt=prompt, temperature=0.7, max_output_tokens=512)
    return response.text.strip()
