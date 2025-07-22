import streamlit as st
import requests

st.set_page_config(page_title="Agentic RAG Chatbot", layout="wide")
st.title("🤖 Agentic RAG Chatbot (MCP)")

BACKEND_URL = "http://localhost:5000"

st.header("1. Upload Documents")
uploaded_files = st.file_uploader("Upload PDF, DOCX, PPTX, CSV, TXT, or MD files", type=["pdf", "docx", "pptx", "csv", "txt", "md"], accept_multiple_files=True)
if st.button("Upload Files") and uploaded_files:
    files = [("files", (f.name, f, f.type)) for f in uploaded_files]
    resp = requests.post(f"{BACKEND_URL}/upload", files=files)
    if resp.ok:
        st.success("Files uploaded and ingested!")
    else:
        st.error("Upload failed.")

st.header("2. Ask Questions")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Your question:")
if st.button("Ask") and user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    data = {"query": user_input}
    resp = requests.post(f"{BACKEND_URL}/ask", json=data)
    if resp.ok:
        result = resp.json()
        answer = result.get("result", {}).get("answer", "No answer.")
        sources = result.get("result", {}).get("sources", [])
        st.session_state.chat_history.append({"role": "assistant", "content": answer, "sources": sources})
    else:
        st.session_state.chat_history.append({"role": "assistant", "content": "Error from backend.", "sources": []})

for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Bot:** {msg['content']}")
        if msg.get("sources"):
            st.markdown(f"_Sources: {', '.join(msg['sources'])}_") 