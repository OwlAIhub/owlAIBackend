from dotenv import load_dotenv
import os
import pinecone

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
pc = pinecone.Pinecone(api_key=api_key)

index_name = "ugc-net-data"
index = pc.Index(index_name)

# DANGER: this deletes everything in your index
index.delete(delete_all=True)

print(f"Index '{index_name}' has been cleared.")
