from database.media_asset import create_media_asset, get_all_media_assets, update_media_asset, delete_media_asset

# Create
media_id = create_media_asset(
    media_type="diagram",
    description="Maslow's Hierarchy Diagram",
    tags=["maslow", "education", "motivation"],
    topic_id="topic_edu_03",
    subject="Education",
    uploaded_by="admin_01",
    file_size_kb=210,
    resolution="1920x1080"
)

# Read
get_all_media_assets()

# Update
update_media_asset(media_id, {"description": "Updated Maslow's Hierarchy", "file_size_kb": 220})

# Delete
delete_media_asset(media_id)
