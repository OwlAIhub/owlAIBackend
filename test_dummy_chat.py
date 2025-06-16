from firebase_admin import credentials, initialize_app, firestore
import uuid

# ✅ Ensure app is initialized
try:
    initialize_app()
except:
    pass

db = firestore.client()

def create_dummy_session(user_id):
    session_id = str(uuid.uuid4())
    session_ref = db.collection("sessions").document(session_id)
    session_data = {
        "session_id": session_id,
        "user_id": user_id,
        "start_time": firestore.SERVER_TIMESTAMP,
        "end_time": None,
        "custom_title": "Test UGC Session",
        "session_type": "study",
        "device_type": "web",
        "question_ids": [],
        "created_at": firestore.SERVER_TIMESTAMP,
        "updated_at": firestore.SERVER_TIMESTAMP
    }

    print(f"\n📥 Writing session:\n{session_data}")
    session_ref.set(session_data)
    print(f"✅ Session {session_id} saved for user: {user_id}")

create_dummy_session("kart8798uyhoinc4r")
