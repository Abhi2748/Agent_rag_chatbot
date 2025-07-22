# Agentic RAG Chatbot for Multi-Format Document QA (MCP)

## Overview
A modular Retrieval-Augmented Generation (RAG) chatbot that supports multi-format document QA using the Model Context Protocol (MCP). It features agent-based orchestration, multi-format ingestion, vector search, and a Streamlit UI for interactive chat.

---

## 📦 Folder Structure
```
/agents         # IngestionAgent, RetrievalAgent, LLMResponseAgent
/ui             # Streamlit interface
/utils          # Helpers (chunking, cleaning, etc.)
/vectorstore    # Embeddings & FAISS vector DB setup
mcp.py          # MCP message format generator
app.py          # Flask orchestrator
```

---

## 🧠 Agents
- **IngestionAgent**: Parses PDF, PPTX, DOCX, CSV, TXT, MD
- **RetrievalAgent**: Embeds content (OpenAI/HF) & retrieves top-K chunks (FAISS)
- **LLMResponseAgent**: Forms prompt with context, calls GPT-4 (OpenAI)

---

## 🧬 MCP Message Format
```python
{
  "sender": "AgentName",
  "receiver": "AgentName",
  "type": "MSG_TYPE",
  "trace_id": "unique-id",
  "payload": {...}
}
```

---

## 🌐 Flask APIs
- `/upload` [POST]: Accepts files, passes to IngestionAgent
- `/ask` [POST]: Accepts query, triggers RetrievalAgent & LLMResponseAgent, returns answer + source

---

## 🖥️ Streamlit UI
- Upload files
- Input multi-turn chat queries
- View answers with source context

---

## 📦 Tech Stack
- Python, OpenAI, Langchain, FAISS, Streamlit, Flask, PyPDF2, python-docx, python-pptx, pandas

---

## 🚀 Setup & Run
```bash
# 1. Clone repo & install dependencies
pip install -r requirements.txt

# 2. Start Flask backend
python app.py

# 3. Start Streamlit UI (in another terminal)
streamlit run ui/streamlit_app.py
```

---

## 🧪 Sample MCP Message Flow
1. **User uploads files** → `/upload` → IngestionAgent parses & chunks → MCP message to RetrievalAgent
2. **User asks question** → `/ask` → RetrievalAgent retrieves context → MCP message to LLMResponseAgent
3. **LLMResponseAgent** forms prompt, calls GPT-4, returns answer + sources

---

## 🧑‍💻 Local Testing
- Access Flask backend at `http://localhost:5000`
- Access Streamlit UI at `http://localhost:8501` 