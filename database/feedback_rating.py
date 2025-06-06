from database.firebase_connection import db
from firebase_admin import firestore
import uuid

# Create a feedback rating
def create_feedback(chat_id, user_id, usefulness_score, content_quality_score, flagged_reason=None, remarks=None):
    feedback_id = str(uuid.uuid4())
    feedback_ref = db.collection("feedback_ratings").document(feedback_id)
    feedback_ref.set({
        "feedback_id": feedback_id,
        "chat_id": chat_id,
        "user_id": user_id,
        "usefulness_score": usefulness_score,
        "content_quality_score": content_quality_score,
        "flagged_reason": flagged_reason,
        "remarks": remarks,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    print(f"Feedback {feedback_id} created successfully!")
    return feedback_id

# Fetch all feedback for a chat
def get_feedback_by_chat(chat_id):
    feedback_ref = db.collection("feedback_ratings").where("chat_id", "==", chat_id)
    docs = feedback_ref.stream()

    print(f"Feedbacks for chat {chat_id}:")
    for doc in docs:
        print(doc.to_dict())

# Update feedback
def update_feedback(feedback_id, updates):
    feedback_ref = db.collection("feedback_ratings").document(feedback_id)
    feedback_ref.update(updates)
    print(f"Feedback {feedback_id} updated successfully!")

# Delete feedback
def delete_feedback(feedback_id):
    feedback_ref = db.collection("feedback_ratings").document(feedback_id)
    feedback_ref.delete()
    print(f"Feedback {feedback_id} deleted successfully!")

# Get flagged chats with usefulness_score == 0
def get_flagged_chats(min_score=0):
    feedback_ref = db.collection("feedback_ratings").where("usefulness_score", "==", min_score)
    docs = feedback_ref.stream()
    flagged = [doc.to_dict() for doc in docs]
    return flagged
