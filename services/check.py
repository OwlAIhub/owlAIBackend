from sentence_transformers import SentenceTransformer

model = SentenceTransformer("Qwen/Qwen3-Embedding-4B")
dummy = model.encode("Hello World")
print("Embedding dimension:", len(dummy))
