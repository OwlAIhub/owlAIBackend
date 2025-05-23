from database.firebase_connection import db
from firebase_admin import firestore
import uuid

ALLOWED_TRAINING_TAGS = {"accuracy", "tone", "relevance"}

# Create an AI training log entry
def create_ai_training_log(prompt_text, ai_response, feedback_score, corrected_by_admin=None, training_tag=None, model_version=None):
    if training_tag and training_tag not in ALLOWED_TRAINING_TAGS:
        raise ValueError(f"Invalid training_tag. Allowed values are {ALLOWED_TRAINING_TAGS}")

    log_id = str(uuid.uuid4())
    log_ref = db.collection("ai_training_logs").document(log_id)
    log_ref.set({
        "log_id": log_id,
        "prompt_text": prompt_text,
        "ai_response": ai_response,
        "feedback_score": feedback_score,
        "corrected_by_admin": corrected_by_admin,
        "training_tag": training_tag,
        "model_version": model_version,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    print(f"AI Training Log {log_id} created successfully!")
    return log_id

# Fetch all training logs
def get_all_ai_training_logs():
    logs_ref = db.collection("ai_training_logs").order_by("timestamp")
    docs = logs_ref.stream()
    print("AI Training Logs:")
    for doc in docs:
        print(doc.to_dict())

# Update training log
def update_ai_training_log(log_id, updates):
    log_ref = db.collection("ai_training_logs").document(log_id)
    log_ref.update(updates)
    print(f"AI Training Log {log_id} updated successfully!")

# Delete training log
def delete_ai_training_log(log_id):
    log_ref = db.collection("ai_training_logs").document(log_id)
    log_ref.delete()
    print(f"AI Training Log {log_id} deleted successfully!")
