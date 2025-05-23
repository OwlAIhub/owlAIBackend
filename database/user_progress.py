from database.firebase_connection import db
from firebase_admin import firestore

# Create or update progress for a topic
def create_or_update_user_progress(user_id, topic_id, completion_percentage=0.0, confidence_level=1, repeated_doubt_ids=None, assessment_scores=None, time_spent_minutes=0):
    progress_ref = db.collection("user_progress").document(f"{user_id}_{topic_id}")
    progress_ref.set({
        "user_id": user_id,
        "topic_id": topic_id,
        "completion_percentage": completion_percentage,
        "confidence_level": confidence_level,
        "last_accessed": firestore.SERVER_TIMESTAMP,
        "repeated_doubt_ids": repeated_doubt_ids if repeated_doubt_ids else [],
        "assessment_scores": assessment_scores if assessment_scores else [],
        "time_spent_minutes": time_spent_minutes,
        "created_at": firestore.SERVER_TIMESTAMP,
        "updated_at": firestore.SERVER_TIMESTAMP
    })
    print(f"User progress for topic {topic_id} created/updated successfully!")

# Fetch all progress for a user
def get_user_progress(user_id):
    progress_ref = db.collection("user_progress").where("user_id", "==", user_id)
    docs = progress_ref.stream()

    print(f"User Progress for user {user_id}:")
    for doc in docs:
        print(doc.to_dict())

# Update progress (partial update)
def update_user_progress(user_id, topic_id, updates):
    progress_ref = db.collection("user_progress").document(f"{user_id}_{topic_id}")
    updates["updated_at"] = firestore.SERVER_TIMESTAMP
    progress_ref.update(updates)
    print(f"User progress for topic {topic_id} updated successfully!")

# Delete progress record
def delete_user_progress(user_id, topic_id):
    progress_ref = db.collection("user_progress").document(f"{user_id}_{topic_id}")
    progress_ref.delete()
    print(f"User progress for topic {topic_id} deleted successfully!")
