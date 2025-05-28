
from sentence_transformers import SentenceTransformer

# Load model once
_model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str) -> list:
    """
    Returns a 384-dim embedding for the input text using MiniLM-L6-v2.
    """
    embedding = _model.encode(text)
    return embedding.tolist()
