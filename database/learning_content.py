from database.firebase_connection import db
from firebase_admin import firestore
import uuid

# Allowed enums
ALLOWED_CONTENT_TYPES = {"diagram", "numerical", "text", "video"}
ALLOWED_CONTENT_STATUS = {"draft", "published", "archived"}

# Create new learning content
def create_learning_content(content_type, metadata, version_control_id=None, linked_asset_ids=None, content_status="draft", review_date=None):
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise ValueError(f"Invalid content_type. Allowed values are {ALLOWED_CONTENT_TYPES}")
    
    if content_status not in ALLOWED_CONTENT_STATUS:
        raise ValueError(f"Invalid content_status. Allowed values are {ALLOWED_CONTENT_STATUS}")

    content_id = str(uuid.uuid4())
    content_ref = db.collection("learning_content").document(content_id)
    content_ref.set({
        "id": content_id,
        "content_type": content_type,
        "metadata": metadata,
        "version_control_id": version_control_id,
        "linked_asset_ids": linked_asset_ids if linked_asset_ids else [],
        "content_status": content_status,
        "review_date": review_date if review_date else None,
        "created_at": firestore.SERVER_TIMESTAMP,
        "updated_at": firestore.SERVER_TIMESTAMP
    })
    print(f" Learning content {content_id} created successfully!")
    return content_id

# Get all learning content
def get_all_learning_content():
    contents_ref = db.collection("learning_content").order_by("created_at")
    docs = contents_ref.stream()

    print("All Learning Content:")
    for doc in docs:
        print(doc.to_dict())

# Update learning content
def update_learning_content(content_id, updates):
    content_ref = db.collection("learning_content").document(content_id)
    updates["updated_at"] = firestore.SERVER_TIMESTAMP
    content_ref.update(updates)
    print(f" Learning content {content_id} updated successfully!")

# Delete learning content
def delete_learning_content(content_id):
    content_ref = db.collection("learning_content").document(content_id)
    content_ref.delete()
    print(f"Learning content {content_id} deleted successfully!")
