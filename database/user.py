from database.firebase_connection import db
from firebase_admin import firestore
import uuid

# Create a new user
def create_user(name, email, mobile_number, gender=None, age_group=None, region=None, exam_ids=None, referral_code=None):
    user_id = str(uuid.uuid4())
    user_ref = db.collection("users").document(user_id)
    user_ref.set({
        "id": user_id,
        "name": name,
        "email": email,
        "mobile_number": mobile_number,
        "gender": gender,
        "age_group": age_group,
        "region": region,
        "exam_ids": exam_ids if exam_ids else [],
        "last_login": firestore.SERVER_TIMESTAMP,
        "referral_code": referral_code,
        "created_at": firestore.SERVER_TIMESTAMP,
        "updated_at": firestore.SERVER_TIMESTAMP
    })
    print(f" User {user_id} created successfully!")
    return user_id

# Get a user
def get_user(user_id):
    user_ref = db.collection("users").document(user_id)
    doc = user_ref.get()
    if doc.exists:
        print(f" User {user_id} data: {doc.to_dict()}")
        return doc.to_dict()
    else:
        print(f" User {user_id} does not exist.")
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
    print(f" User {user_id} deleted successfully!")
