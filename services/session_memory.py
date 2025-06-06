# services/session_memory.py

from collections import defaultdict

session_memory = defaultdict(dict)

def update_session_topic(session_id: str, topic: str, aspect: str = None):
    session_memory[session_id]["current_topic"] = topic
    if aspect:
        session_memory[session_id]["last_aspect"] = aspect

def get_session_topic(session_id: str):
    return session_memory.get(session_id, {}).get("current_topic", None)

def get_last_aspect(session_id: str):
    return session_memory.get(session_id, {}).get("last_aspect", None)

def reset_session_memory(session_id: str):
    if session_id in session_memory:
        del session_memory[session_id]
