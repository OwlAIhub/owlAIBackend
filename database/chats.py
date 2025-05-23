from database.firebase_connection import db
from firebase_admin import firestore
import uuid

# Create a new chat entry
def save_chat(user_id, subject, unit, topic, sub_topic, question_text, response_text, source_ref_type, source_ref_id=None, media_type=None, media_url=None, topic_tags=None, feedback_rating=None):
    chat_id = str(uuid.uuid4())
    chat_ref = db.collection("chats").document(chat_id)
    chat_ref.set({
        "chat_id": chat_id,
        "user_id": user_id,
        "subject": subject,
        "unit": unit,
        "topic": topic,
        "sub_topic": sub_topic,
        "question_text": question_text,
        "response_text": response_text,
        "timestamp": firestore.SERVER_TIMESTAMP,
        "source_ref_type": source_ref_type,
        "source_ref_id": source_ref_id,
        "media_type": media_type,
        "media_url": media_url,
        "topic_tags": topic_tags if topic_tags else [],
        "feedback_rating": feedback_rating,
        "created_at": firestore.SERVER_TIMESTAMP,
        "updated_at": firestore.SERVER_TIMESTAMP
    })
    print(f"Chat {chat_id} saved successfully!")
    return chat_id

# Get all chats for a user
def get_chat_history(user_id):
    chats_ref = db.collection("chats").where("user_id", "==", user_id).order_by("timestamp")
    docs = chats_ref.stream()

    print(f"Chat History for user {user_id}:")
    for doc in docs:
        print(doc.to_dict())

# Delete a chat
def delete_chat(chat_id):
    chat_ref = db.collection("chats").document(chat_id)
    chat_ref.delete()
    print(f"Chat {chat_id} deleted successfully!")
