from database.learning_content import create_learning_content, get_all_learning_content, update_learning_content, delete_learning_content
from firebase_admin import firestore

# Step 1: Create learning content
metadata = {
    "title": "Photosynthesis Introduction",
    "subject": "Biology",
    "topic": "Plant Physiology",
    "summary": "Photosynthesis allows green plants to create food from sunlight."
}

content_id = create_learning_content(
    content_type="text",
    metadata=metadata,
    version_control_id="v1",
    linked_asset_ids=["asset123", "asset456"],
    content_status="published",
    review_date=firestore.SERVER_TIMESTAMP
)

# Step 2: Get all learning content
get_all_learning_content()

# Step 3: Update a learning content entry
update_learning_content(content_id, {"content_status": "archived"})

# Step 4: Delete a learning content entry (optional)
# delete_learning_content(content_id)
