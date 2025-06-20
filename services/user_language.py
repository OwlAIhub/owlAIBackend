from database.firebase_connection import db

def get_user_language(user_id):
    doc = db.collection("users").document(user_id).get()
    if doc.exists:
        return doc.to_dict().get("language", "HINGLISH")
    return "HINGLISH"
