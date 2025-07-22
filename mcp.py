import uuid

def generate_mcp_message(sender, receiver, msg_type, payload, trace_id=None):
    if trace_id is None:
        trace_id = str(uuid.uuid4())
    return {
        "sender": sender,
        "receiver": receiver,
        "type": msg_type,
        "trace_id": trace_id,
        "payload": payload
    } 