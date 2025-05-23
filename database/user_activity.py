from database.firebase_connection import db
from firebase_admin import firestore
import uuid

# Create a user activity log
def create_user_activity(session_id, user_id, question_log, confusion_flag=False, auto_generated_tags=None, language_pattern=None, session_duration=0):
    activity_id = str(uuid.uuid4())
    activity_ref = db.collection("user_activity").document(activity_id)
    activity_ref.set({
        "activity_id": activity_id,
        "session_id": session_id,
        "user_id": user_id,
        "question_log": question_log,  # Ideally stored as TSVECTOR/text blob
        "confusion_flag": confusion_flag,
        "auto_generated_tags": auto_generated_tags if auto_generated_tags else [],
        "language_pattern": language_pattern,
        "session_duration": session_duration,
        "created_at": firestore.SERVER_TIMESTAMP,
        "updated_at": firestore.SERVER_TIMESTAMP
    })
    print(f"User Activity {activity_id} logged successfully!")
    return activity_id

# Fetch all user activities
def get_all_user_activities():
    activity_ref = db.collection("user_activity").order_by("created_at")
    docs = activity_ref.stream()
    print("User Activities:")
    for doc in docs:
        print(doc.to_dict())

# Update user activity
def update_user_activity(activity_id, updates):
    activity_ref = db.collection("user_activity").document(activity_id)
    updates["updated_at"] = firestore.SERVER_TIMESTAMP
    activity_ref.update(updates)
    print(f"User Activity {activity_id} updated successfully!")

# Delete user activity
def delete_user_activity(activity_id):
    activity_ref = db.collection("user_activity").document(activity_id)
    activity_ref.delete()
    print(f"User Activity {activity_id} deleted successfully!")
