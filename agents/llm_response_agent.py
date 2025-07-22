import os
from typing import List, Dict, Any
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
load_dotenv()

class LLMResponseAgent:
    def __init__(self):
        self.model = os.getenv("LLM_MODEL", "HuggingFaceH4/zephyr-7b-beta")
        api_key = os.getenv("HF_TOKEN")
        if not api_key:
            raise EnvironmentError("Hugging Face API token not found! Please set HF_TOKEN in your environment or .env file.")
        self.client = InferenceClient(
            provider="auto",
            api_key=api_key
        )

    def answer(self, query: str, context: List[Dict[str, Any]], trace_id: str) -> Dict[str, Any]:
        context_text = "\n\n".join([f"Source: {c['source']}\n{c['chunk']}" for c in context])
        prompt = f"""
You are a helpful assistant. Use the following context to answer the user's question. Cite sources.

Context:
{context_text}

Question: {query}
Answer (with sources):
"""
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        answer = completion.choices[0].message.content
        return {
            'answer': answer,
            'sources': [c['source'] for c in context],
            'trace_id': trace_id
        } 