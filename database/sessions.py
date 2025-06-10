from database.firebase_connection import db
from firebase_admin import firestore
import uuid

# Create a new session
def create_session(user_id, session_type="study", device_type="mobile", ip_address="0.0.0.0", question_ids=None):
    session_id = str(uuid.uuid4())
    session_ref = db.collection("sessions").document(session_id)
    session_ref.set({
        "session_id": session_id,
        "user_id": user_id,
        "start_time": firestore.SERVER_TIMESTAMP,
        "end_time": None,
        "question_ids": question_ids if question_ids else [],
        "session_type": session_type,
        "device_type": device_type,
        "ip_address": ip_address,
        "created_at": firestore.SERVER_TIMESTAMP,
        "updated_at": firestore.SERVER_TIMESTAMP,
        
        "learning_state": {
            "current_unit": "UGC NET",
            "current_subtopic": "Introduction",
            "learning_stage": "explanation",
            "has_done_quiz": False,
            "last_question_type": "None"
        },
        "history": [],
        "quiz_state": {}
    })
    print(f"Session {session_id} started for user {user_id}!")
    return session_id


# Update session (e.g., adding questions, marking end time)
def update_session(session_id, updates):
    session_ref = db.collection("sessions").document(session_id)
    updates["updated_at"] = firestore.SERVER_TIMESTAMP
    session_ref.update(updates)
    print(f"Session {session_id} updated successfully!")

# End a session
def end_session(session_id):
    session_ref = db.collection("sessions").document(session_id)
    session_ref.update({
        "end_time": firestore.SERVER_TIMESTAMP,
        "updated_at": firestore.SERVER_TIMESTAMP
    })
    print(f"Session {session_id} ended.")

# Get all sessions by user, newest first
def get_sessions_by_user(user_id):
    sessions_ref = db.collection("sessions").where("user_id", "==", user_id).order_by("start_time", direction=firestore.Query.DESCENDING).stream()
    for doc in sessions_ref:
        return doc.to_dict()
    return None

# Rename session (used for custom titles)
def rename_session(session_id, new_name):
    session_ref = db.collection("sessions").document(session_id)
    session_ref.update({
        "custom_title": new_name,
        "updated_at": firestore.SERVER_TIMESTAMP
    })
    print(f"Session {session_id} renamed to {new_name}")

# Delete session
def delete_session(session_id):
    db.collection("sessions").document(session_id).delete()
    print(f"Session {session_id} deleted")
