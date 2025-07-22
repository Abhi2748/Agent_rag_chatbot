import os
from pinecone import Pinecone
from typing import List, Dict, Any
from pinecone import ServerlessSpec
from dotenv import load_dotenv
load_dotenv()


from openai import OpenAI

class RetrievalAgent:
    def __init__(self):
        self.api_key = os.getenv("PINECONE_API_KEY")
        self.index_name = os.getenv("PINECONE_INDEX", "developer-quickstart-py")
        self.cloud = os.getenv("PINECONE_CLOUD", "aws")
        self.region = os.getenv("PINECONE_REGION", "us-east-1")
        self.model = os.getenv("PINECONE_EMBED_MODEL", "llama-text-embed-v2")
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.pc = Pinecone(api_key=self.api_key)
        if self.pc.has_index(self.index_name):
            self.pc.delete_index(self.index_name)
        print(f"Creating index '{self.index_name}' with dimension 1536...")
        self.pc.create_index(
            name=self.index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud=self.cloud, region=self.region)
            )
        self.index = self.pc.Index(self.index_name)

        


    def embed(self, text: str) -> list:
        response = self.client.embeddings.create(
            input=[text],
            model="text-embedding-ada-002"
        )
        return response.data[0].embedding



    def build_index(self, chunks: List[Dict[str, Any]]):
        items = []
        for i, c in enumerate(chunks):
            embedding = self.embed(c['chunk'])
            items.append({
                "id": f"chunk-{i}",
                "values": embedding,
                "metadata": {"chunk_text": c['chunk'], "source": c['source'], "trace_id": c['trace_id']}
             })
        self.index.upsert(items)

    def retrieve(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        query_embedding = self.embed(query)

        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        output = []
        for match in results['matches']:
            meta = match['metadata']
            output.append({
                'chunk': meta.get('chunk_text', ''),
                'source': meta.get('source', ''),
                'score': match.get('score', 0)
            })
        return output 