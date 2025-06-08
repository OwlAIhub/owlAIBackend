import firebase_admin
from firebase_admin import credentials, firestore
import os

# Load Firebase credentials and initialize app
if not firebase_admin._apps:
    cred = credentials.Certificate("owl-ai-1ef31-firebase-adminsdk-fbsvc-4788ce64d5.json")
    firebase_admin.initialize_app(cred)

# Initialize Firestore DB client
db = firestore.client()


# 🔍 Get full session data
def get_session_state(session_id: str):
    try:
        doc_ref = db.collection("sessions").document(session_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return {}
    except Exception as e:
        print("[Firestore] get_session_state Error:", str(e))
        return {}


# 🧾 Save a new message pair to history
def add_to_history(session_id: str, message_pair: dict):
    try:
        doc_ref = db.collection("sessions").document(session_id)
        current = get_session_state(session_id)
        history = current.get("history", [])
        history.append(message_pair)
        doc_ref.set({"history": history}, merge=True)
    except Exception as e:
        print("[Firestore] add_to_history Error:", str(e))


# 🧹 Reset a session
def clear_session(session_id: str):
    try:
        db.collection("sessions").document(session_id).set({}, merge=True)
    except Exception as e:
        print("[Firestore] clear_session Error:", str(e))


# 🧠 Set active topic or quiz mode
def set_session_data(session_id: str, updates: dict):
    try:
        db.collection("sessions").document(session_id).set(updates, merge=True)
    except Exception as e:
        print("[Firestore] set_session_data Error:", str(e))
