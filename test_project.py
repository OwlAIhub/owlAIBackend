from database.project import create_project, get_projects, update_project, delete_project

# Create a sample project
project_id = create_project(
    user_id="user_001",
    title="Medieval India Important Notes",
    subject="History",
    unit="Medieval India",
    topic="Bhakti Movement",
    sub_topic="Saint Poets",
    saved_content_ids=["content_123", "content_456"],
    notes=["Focus on Kabir's teachings", "Understand the regional variations"]
)

# Get projects for user
get_projects("user_001")

# Update the project (optional)
update_project(project_id, {"notes": ["Updated notes content."]})

# Delete project (optional)
# delete_project(project_id)
