import firebase_admin


from database.sessions import update_session, get_sessions_by_user, create_session

from firebase_admin import credentials, firestore


# 📦 Initialize Firebase App
if not firebase_admin._apps:
    cred = credentials.Certificate("owl-ai-1ef31-firebase-adminsdk-fbsvc-4788ce64d5.json")
    firebase_admin.initialize_app(cred)

# 🔧 Firestore DB reference
db = firestore.client()

# 🔍 Get full session data
def get_session_state(session_id: str) -> dict:
    try:
        doc_ref = db.collection("sessions").document(session_id)
        doc = doc_ref.get()
        return doc.to_dict() if doc.exists else {}
    except Exception as e:
        print("[Firestore] get_session_state Error:", str(e))
        return {}

# 💾 Update (overwrite) entire session state
def update_session_state(session_id: str, new_data: dict):
    try:
        db.collection("sessions").document(session_id).set(new_data)
    except Exception as e:
        print("[Firestore] update_session_state Error:", str(e))

# 🧾 Add a new message pair to chat history
def add_to_history(session_id: str, message_pair: dict):
    try:
        current = get_session_state(session_id)
        history = current.get("history", [])
        history.append(message_pair)
        db.collection("sessions").document(session_id).set({"history": history}, merge=True)
    except Exception as e:
        print("[Firestore] add_to_history Error:", str(e))

# 🧹 Reset a session (clears everything)
def clear_session(session_id: str):
    try:
        db.collection("sessions").document(session_id).set({}, merge=True)
    except Exception as e:
        print("[Firestore] clear_session Error:", str(e))

# 🎯 Dynamically update specific fields (e.g., topic, quiz_mode)
def set_session_data(session_id: str, updates: dict):
    try:
        db.collection("sessions").document(session_id).set(updates, merge=True)
    except Exception as e:
        print("[Firestore] set_session_data Error:", str(e))

# 📚 QUIZ SESSION MANAGEMENT

def save_quiz_session(session_id: str, quiz_obj: dict):
    memory = get_session_state(session_id)
    memory["quiz_session"] = quiz_obj
    update_session_state(session_id, memory)

def get_quiz_session(session_id: str):
    memory = get_session_state(session_id)
    return memory.get("quiz_session", None)

def clear_quiz_session(session_id: str):
    memory = get_session_state(session_id)
    if "quiz_session" in memory:
        del memory["quiz_session"]
    update_session_state(session_id, memory)



def add_learned_topic(session_id: str, topic: str):
    memory = get_session_state(session_id)
    learned = memory.get("learned_topics", [])
    if topic not in learned:
        learned.append(topic)
        set_session_data(session_id, {"learned_topics": learned})


def get_learning_state(session_id: str) -> dict:
    try:
        session = get_session_state(session_id)
        return session.get("learning_state", {
            "current_unit": "UGC NET",
            "current_subtopic": "Introduction",
            "learning_stage": "explanation",
            "has_done_quiz": False,
            "last_question_type": "None"
        })
    except Exception as e:
        print("[Firestore] get_learning_state Error:", str(e))
        return {}

 # import this


def update_learning_state(session_id: str, new_learning_state: dict):
    """
    Upsert the learning_state for a given session.
    Uses Firestore set(..., merge=True) so it creates the document if missing.
    """
    session_ref = db.collection("sessions").document(session_id)

    # Prepare the merge data
    merge_data = {
        "learning_state": new_learning_state,
        "updated_at": firestore.SERVER_TIMESTAMP
    }
    # Upsert learning_state (will create document if it doesn't exist)
    session_ref.set(merge_data, merge=True)

    print(f"Session {session_id} learning_state updated: {new_learning_state}")




def reset_learning_state(session_id: str):
    try:
        default = {
            "current_unit": "UGC NET",
            "current_subtopic": "Introduction",
            "learning_stage": "explanation",
            "has_done_quiz": False,
            "last_question_type": "None"
        }
        set_session_data(session_id, {"learning_state": default})
    except Exception as e:
        print("[Firestore] reset_learning_state Error:", str(e))
