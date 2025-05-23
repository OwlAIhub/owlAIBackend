from database.firebase_connection import db
from firebase_admin import firestore
import uuid

# Create a new glossary term
def create_glossary_term(user_id, term, definition, subject, unit, topic, sub_topic, user_mention_ids=None, linked_chat_ids=None):
    term_id = str(uuid.uuid4())
    term_ref = db.collection("glossary_terms").document(term_id)
    term_ref.set({
        "term_id": term_id,
        "user_id": user_id,
        "term": term,
        "definition": definition,
        "subject": subject,
        "unit": unit,
        "topic": topic,
        "sub_topic": sub_topic,
        "user_mention_ids": user_mention_ids if user_mention_ids else [],
        "linked_chat_ids": linked_chat_ids if linked_chat_ids else [],
        "created_at": firestore.SERVER_TIMESTAMP,
        "updated_at": firestore.SERVER_TIMESTAMP
    })
    print(f"Glossary term {term_id} created successfully!")
    return term_id

# Get all glossary terms for a user
def get_glossary_terms(user_id):
    terms_ref = db.collection("glossary_terms").where("user_id", "==", user_id).order_by("created_at")
    docs = terms_ref.stream()

    print(f"Glossary Terms for user {user_id}:")
    for doc in docs:
        print(doc.to_dict())

# Update a glossary term
def update_glossary_term(term_id, updates):
    term_ref = db.collection("glossary_terms").document(term_id)
    updates["updated_at"] = firestore.SERVER_TIMESTAMP
    term_ref.update(updates)
    print(f"Glossary term {term_id} updated successfully!")

# Delete a glossary term
def delete_glossary_term(term_id):
    term_ref = db.collection("glossary_terms").document(term_id)
    term_ref.delete()
    print(f"Glossary term {term_id} deleted successfully!")
