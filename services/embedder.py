from sentence_transformers import SentenceTransformer

# Load model once
_model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str) -> list:
    try:
        embedding = _model.encode(text)
        return embedding.tolist()
    except Exception as e:
        print(f"[Embedding Error] {str(e)}")
        return []
