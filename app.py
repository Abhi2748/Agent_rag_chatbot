from flask import Flask, request, jsonify
from mcp import generate_mcp_message
import uuid
from agents.ingestion_agent import IngestionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.llm_response_agent import LLMResponseAgent
import traceback


app = Flask(__name__)

retrieval_agent = RetrievalAgent()
llm_agent = LLMResponseAgent()
chunks_db = []

@app.route('/upload', methods=['POST'])
def upload():
    print("[UPLOAD] POST /upload called")
    try:
        files = request.files.getlist('files')
        if not files or len(files) == 0:
            print("[UPLOAD] No files received.")
            return jsonify({"status": "error", "error": "No files uploaded."}), 400
        print(f"[UPLOAD] Received {len(files)} files: {[f.filename for f in files]}")
        trace_id = str(uuid.uuid4())
        try:
            chunks = IngestionAgent.process(files, trace_id)
        except Exception as e:
            print(f"[UPLOAD] IngestionAgent error: {e}")
            traceback.print_exc()
            return jsonify({"status": "error", "error": f"File parsing error: {e}"}), 500
        if not chunks:
            print("[UPLOAD] No valid chunks extracted from files.")
            return jsonify({"status": "error", "error": "No valid content found in uploaded files."}), 400
        global chunks_db
        chunks_db = chunks
        try:
            retrieval_agent.build_index(chunks)
        except Exception as e:
            print(f"[UPLOAD] Pinecone error: {e}")
            traceback.print_exc()
            return jsonify({"status": "error", "error": f"Vector DB error: {e}"}), 500
        mcp_msg = generate_mcp_message(
            sender="FlaskAPI",
            receiver="IngestionAgent",
            msg_type="UPLOAD",
            payload={"filenames": [f.filename for f in files], "num_chunks": len(chunks)},
            trace_id=trace_id
        )
        result = {"status": "success", "trace_id": trace_id, "msg": mcp_msg, "num_chunks": len(chunks)}
        print(f"[UPLOAD] Success: {result}")
        return jsonify(result)
    except Exception as e:
        print(f"[UPLOAD] General error: {e}")
        traceback.print_exc()
        return jsonify({"status": "error", "error": f"Unexpected error: {e}"}), 500

@app.route('/ask', methods=['POST'])
def ask():
    print("[ASK] POST /ask called")
    try:
        data = request.json
        print(f"[ASK] Received data: {data}")
        query = data.get('query')
        trace_id = str(uuid.uuid4())
        mcp_msg = generate_mcp_message(
            sender="FlaskAPI",
            receiver="RetrievalAgent",
            msg_type="QUERY",
            payload={"query": query},
            trace_id=trace_id
        )
        context = retrieval_agent.retrieve(query, top_k=4)
        print(f"[ASK] Retrieved context: {context}")
        answer = llm_agent.answer(query, context, trace_id)
        print(f"[ASK] LLM answer: {answer}")
        return jsonify({"trace_id": trace_id, "msg": mcp_msg, "result": answer})
    except Exception as e:
        print(f"[ASK] Error: {e}")
        traceback.print_exc()
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == '__main__':
    print("[INFO] Flask app starting...")
    app.run(debug=True) 