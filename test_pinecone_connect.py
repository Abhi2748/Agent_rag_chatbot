import os
from pinecone import Pinecone
from dotenv import load_dotenv

# Load .env variables
load_dotenv()


# Set your Pinecone API key and index name here or via environment variables
api_key = os.getenv("PINECONE_API_KEY", "your-pinecone-api-key")
index_name = os.getenv("PINECONE_INDEX", "quickstart")

# Initialize Pinecone client
pc = Pinecone(api_key=api_key)
index = pc.Index(index_name)

# Upsert a sample vector
sample_id = "vec1"
sample_vector = [0.1] * 1024  # 1024-dim vector (adjust if your index uses a different dimension)
index.upsert([
    {"id": sample_id, "values": sample_vector, "metadata": {"test": "yes"}}
])
print(f"Upserted vector with id {sample_id}")

# Query the vector
result = index.query(vector=sample_vector, top_k=1, include_metadata=True)
print("Query result:", result) 