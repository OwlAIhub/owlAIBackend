from database.firebase_connection import db
from firebase_admin import firestore
import uuid

ALLOWED_MEDIA_TYPES = {"image", "diagram", "numerical", "audio"}

# Create a new media asset
def create_media_asset(media_type, description, tags, topic_id, subject, uploaded_by, file_size_kb, resolution):
    if media_type not in ALLOWED_MEDIA_TYPES:
        raise ValueError(f"Invalid media_type. Allowed values are {ALLOWED_MEDIA_TYPES}")

    media_id = str(uuid.uuid4())
    media_ref = db.collection("media_assets").document(media_id)
    media_ref.set({
        "media_id": media_id,
        "type": media_type,
        "description": description,
        "tags": tags if tags else [],
        "topic_id": topic_id,
        "subject": subject,
        "uploaded_by": uploaded_by,
        "file_size_kb": file_size_kb,
        "resolution": resolution,
        "created_on": firestore.SERVER_TIMESTAMP
    })
    print(f"Media Asset {media_id} created successfully!")
    return media_id

# Get all media assets
def get_all_media_assets():
    media_ref = db.collection("media_assets").order_by("created_on")
    docs = media_ref.stream()
    print("Media Assets:")
    for doc in docs:
        print(doc.to_dict())

# Update media asset
def update_media_asset(media_id, updates):
    media_ref = db.collection("media_assets").document(media_id)
    updates["updated_at"] = firestore.SERVER_TIMESTAMP
    media_ref.update(updates)
    print(f"Media Asset {media_id} updated successfully!")

# Delete media asset
def delete_media_asset(media_id):
    media_ref = db.collection("media_assets").document(media_id)
    media_ref.delete()
    print(f"Media Asset {media_id} deleted successfully!")
