import os
import glob
import uuid
from agents.ingestion_agent import IngestionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.llm_response_agent import LLMResponseAgent
from mcp import generate_mcp_message

# 1. Ingest all files in a folder
def ingest_folder(folder_path):
    files = []
    file_paths = glob.glob(os.path.join(folder_path, "*"))
    print("Files found:", file_paths)
    for file_path in file_paths:
        ext = os.path.splitext(file_path)[-1].lower()
        if ext in IngestionAgent.SUPPORTED_FORMATS:
            files.append(open(file_path, "rb"))
    trace_id = str(uuid.uuid4())
    chunks = IngestionAgent.process(files, trace_id)
    for f in files:
        f.close()
    return chunks, trace_id

def main():
    folder = input("Enter path to folder with documents: ").strip()
    print(f"Ingesting files from {folder} ...")
    chunks, trace_id = ingest_folder(folder)
    if not chunks:
        print("[ERROR] No valid chunks ingested from the provided files. Exiting.")
        return
    print(f"Ingested {len(chunks)} chunks.")

    retrieval_agent = RetrievalAgent()
    try:
        retrieval_agent.build_index(chunks)
    except Exception as e:
        print(f"[ERROR] Pinecone upsert failed: {e}")
        return
    print("Vector index built.")

    llm_agent = LLMResponseAgent()

    while True:
        query = input("\nAsk a question (or type 'exit'): ").strip()
        if query.lower() == "exit":
            break
        mcp_msg = generate_mcp_message(
            sender="CLI",
            receiver="RetrievalAgent",
            msg_type="QUERY",
            payload={"query": query},
            trace_id=trace_id
        )
        context = retrieval_agent.retrieve(query, top_k=4)
        answer = llm_agent.answer(query, context, trace_id)
        print("\n--- Answer ---")
        print(answer['answer'])
        print("Sources:", answer['sources'])

if __name__ == "__main__":
    main() 