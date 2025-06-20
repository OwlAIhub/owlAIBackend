from database.firebase_connection import db
from firebase_admin import firestore
import uuid

# Create a new user
def create_user(
    first_name,
    last_name,
    email,
    mobile_number,
    curriculum,
    exam_cycle,
    attempt,
    language,
    selected_subjects,
    exam_ids,
    submitted_at,
    heard_from=None,
    other_subject=None,
    gender=None,
    age_group=None,
    region=None,
    referral_code=None
):
    user_id = str(uuid.uuid4())  
    user_ref = db.collection("users").document(user_id)
    user_ref.set({
        "uid": user_id,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "mobile_number": mobile_number,
        "curriculum": curriculum,
        "exam_cycle": exam_cycle,
        "attempt": attempt,
        "language": language,
        "selected_subjects": selected_subjects,
        "exam_ids": exam_ids if exam_ids else [],
        "submitted_at": submitted_at,
        "heard_from": heard_from,
        "other_subject": other_subject,
        "gender": gender,
        "age_group": age_group,
        "region": region,
        "referral_code": referral_code,
        "created_at": firestore.SERVER_TIMESTAMP,
        "updated_at": firestore.SERVER_TIMESTAMP
    })
    print(f"User {user_id} created successfully!")
    return user_id

# Get a user
def get_user(user_id):
    user_ref = db.collection("users").document(user_id)
    doc = user_ref.get()
    if doc.exists:
        print(f"User {user_id} data: {doc.to_dict()}")
        return doc.to_dict()
    else:
        print(f"User {user_id} does not exist.")
        return None

# Update a user
def update_user(user_id, updates):
    user_ref = db.collection("users").document(user_id)
    updates["updated_at"] = firestore.SERVER_TIMESTAMP
    user_ref.update(updates)
    print(f"User {user_id} updated successfully!")

# Delete a user
def delete_user(user_id):
    user_ref = db.collection("users").document(user_id)
    user_ref.delete()
    print(f"User {user_id} deleted successfully!")

# Check for duplicate mobile
def is_mobile_registered(mobile_number):
    users_ref = db.collection("users")
    query = users_ref.where("mobile_number", "==", mobile_number).get()
    return len(query) > 0


def get_user_language(user_id: str) -> str:
    db = firestore.client()
    doc = db.collection("users").document(user_id).get()
    if doc.exists:
        return doc.to_dict().get("language", "HINGLISH")
    return "HINGLISH"
