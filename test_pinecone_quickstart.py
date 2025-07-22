import os
from pinecone import Pinecone
from dotenv import load_dotenv

# Load .env variables
load_dotenv()


# Load Pinecone API key and index name from environment variables
api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX", "quickstart")

if not api_key:
    raise ValueError("PINECONE_API_KEY not set in environment or .env file.")

# Initialize Pinecone client
pc = Pinecone(api_key=api_key)

# Create the index if it doesn't exist
if not pc.has_index(index_name):
    print(f"Index '{index_name}' does not exist. Creating it...")
    pc.create_index(
        name=index_name,
        dimension=1024,
        metric="cosine",
        cloud="aws",
        region="us-east-1"
    )
else:
    print(f"Index '{index_name}' already exists.")

index = pc.Index(index_name)

# Upsert a sample vector (dimension 1024)
sample_id = "vec1"
sample_vector = [0.1] * 1024
index.upsert([
    {"id": sample_id, "values": sample_vector, "metadata": {"test": "yes"}}
])
print(f"Upserted vector with id {sample_id}")

# Query the vector
result = index.query(vector=sample_vector, top_k=1, include_metadata=True)
print("Query result:", result) 