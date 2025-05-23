from database.firebase_connection import db
from firebase_admin import firestore
import uuid

# Create a new project
def create_project(user_id, title, subject, unit, topic, sub_topic, saved_content_ids=None, notes=None):
    project_id = str(uuid.uuid4())
    project_ref = db.collection("projects").document(project_id)
    project_ref.set({
        "project_id": project_id,
        "user_id": user_id,
        "title": title,
        "subject": subject,
        "unit": unit,
        "topic": topic,
        "sub_topic": sub_topic,
        "saved_content_ids": saved_content_ids if saved_content_ids else [],
        "notes": notes if notes else [],
        "created_on": firestore.SERVER_TIMESTAMP,
        "updated_at": firestore.SERVER_TIMESTAMP
    })
    print(f"Project {project_id} created successfully!")
    return project_id

# Get all projects for a user
def get_projects(user_id):
    projects_ref = db.collection("projects").where("user_id", "==", user_id).order_by("created_on")
    docs = projects_ref.stream()

    print(f"Projects for user {user_id}:")
    for doc in docs:
        print(doc.to_dict())

# Update a project
def update_project(project_id, updates):
    project_ref = db.collection("projects").document(project_id)
    updates["updated_at"] = firestore.SERVER_TIMESTAMP
    project_ref.update(updates)
    print(f"Project {project_id} updated successfully!")

# Delete a project
def delete_project(project_id):
    project_ref = db.collection("projects").document(project_id)
    project_ref.delete()
    print(f"Project {project_id} deleted successfully!")
 