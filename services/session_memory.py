from collections import defaultdict

# In-memory session storage
session_memory = defaultdict(dict)

def update_session_topic(session_id: str, topic: str, aspect: str = None):
    session_memory[session_id]["current_topic"] = topic
    if aspect:
        session_memory[session_id]["last_aspect"] = aspect

def get_session_topic(session_id: str):
    return session_memory.get(session_id, {}).get("current_topic", None)

def get_last_aspect(session_id: str):
    return session_memory.get(session_id, {}).get("last_aspect", None)

def set_last_mood(session_id: str, mood: str):
    session_memory[session_id]["last_mood"] = mood

def get_last_mood(session_id: str):
    return session_memory.get(session_id, {}).get("last_mood", None)

def set_active_quiz_topic(session_id: str, topic: str):
    session_memory[session_id]["active_quiz_topic"] = topic

def get_active_quiz_topic(session_id: str):
    return session_memory.get(session_id, {}).get("active_quiz_topic", None)

def start_quiz(session_id: str, topic: str):
    session_memory[session_id]["quiz"] = {
        "topic": topic,
        "score": 0,
        "index": 0,
        "questions": [],
        "answers": [],
        "mode": "ask"
    }

def get_quiz_state(session_id: str):
    return session_memory.get(session_id, {}).get("quiz", None)

def update_quiz_state(session_id: str, quiz_data: dict):
    session_memory[session_id]["quiz"] = quiz_data

def reset_quiz(session_id: str):
    if "quiz" in session_memory.get(session_id, {}):
        del session_memory[session_id]["quiz"]

def reset_session_memory(session_id: str):
    if session_id in session_memory:
        del session_memory[session_id]
