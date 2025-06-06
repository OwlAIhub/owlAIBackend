from database.firebase_connection import db
from services.llm import get_response_from_llm
from firebase_admin import firestore

def retry_failed_answer(chat_id: str) -> str:
    chat_ref = db.collection("chats").document(chat_id)
    chat_doc = chat_ref.get()

    if not chat_doc.exists:
        raise ValueError(f"Chat with ID {chat_id} not found.")

    chat = chat_doc.to_dict()
    question = chat.get("question_text", "")
    old_response = chat.get("response_text", "")

    retry_prompt = (
        f"The following answer received negative feedback:\n\n"
        f"Q: {question}\nA: {old_response}\n\n"
        "Improve this answer with clearer explanation, structure, and relevant examples:"
    )

    improved_answer = get_response_from_llm(retry_prompt)

    chat_ref.update({
        "response_text": improved_answer,
        "updated_at": firestore.SERVER_TIMESTAMP
    })

    return improved_answer
