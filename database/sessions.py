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
        "updated_at": firestore.SERVER_TIMESTAMP
    })
    print(f"Session {session_id} started for user {user_id}!")
    return session_id

# Update session (e.g., adding questions, marking end time)
def update_session(session_id, updates):
    session_ref = db.collection("sessions").document(session_id)
    updates["updated_at"] = firestore.SERVER_TIMESTAMP
    session_ref.update(updates)
    print(f" Session {session_id} updated successfully!")

# End a session
def end_session(session_id):
    session_ref = db.collection("sessions").document(session_id)
    session_ref.update({
        "end_time": firestore.SERVER_TIMESTAMP,
        "updated_at": firestore.SERVER_TIMESTAMP
    })
    print(f" Session {session_id} ended.")
