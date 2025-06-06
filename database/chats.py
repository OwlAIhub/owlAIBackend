from database.firebase_connection import db
from firebase_admin import firestore
import uuid

def save_chat(session_id, user_id, subject, unit, topic, sub_topic, question_text, response_text, source_ref_type, source_ref_id=None, media_type=None, media_url=None, topic_tags=None, feedback_rating=None, title=None, intent=None, is_professional=False ):
    if not response_text or response_text.strip() == "":
        print("Skipping chat save: response_text is empty.")
        return None

    chat_id = str(uuid.uuid4())
    chat_ref = db.collection("chats").document(chat_id)
    chat_ref.set({
        "chat_id": chat_id,
        "session_id": session_id,
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
        "title": title or question_text[:40],
        "intent": intent,
        "is_professional": is_professional,
        "created_at": firestore.SERVER_TIMESTAMP,
        "updated_at": firestore.SERVER_TIMESTAMP
    })
    print(f"Chat {chat_id} saved successfully!")
    return chat_id

def get_chat_history(user_id):
    chats_ref = db.collection("chats").where("user_id", "==", user_id).order_by("timestamp")
    docs = chats_ref.stream()
    return [doc.to_dict() for doc in docs]

def delete_chat(chat_id):
    chat_ref = db.collection("chats").document(chat_id)
    chat_ref.delete()
    print(f"Chat {chat_id} deleted successfully!")


def delete_chats_by_session(session_id):
    chats_ref = db.collection("chats").where("session_id", "==", session_id)
    docs = chats_ref.stream()
    for doc in docs:
        doc.reference.delete()
    print(f"All chats in session {session_id} deleted")
def get_chat_history_by_session(session_id):
    chats_ref = db.collection("chats").where("session_id", "==", session_id).order_by("timestamp")
    docs = chats_ref.stream()
    return [doc.to_dict() for doc in docs]
