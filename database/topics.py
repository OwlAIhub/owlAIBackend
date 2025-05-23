from database.firebase_connection import db
from firebase_admin import firestore
import uuid

# Create a new topic
def create_topic(subject_id, name, unit_index, related_topic_ids=None, prerequisites=None, learning_objectives=None, is_active=True):
    topic_id = str(uuid.uuid4())
    topic_ref = db.collection("topics").document(topic_id)
    topic_ref.set({
        "id": topic_id,
        "subject_id": subject_id,
        "name": name,
        "unit_index": unit_index,
        "related_topic_ids": related_topic_ids if related_topic_ids else [],
        "prerequisites": prerequisites if prerequisites else [],
        "learning_objectives": learning_objectives if learning_objectives else [],
        "is_active": is_active,
        "created_at": firestore.SERVER_TIMESTAMP,
        "updated_at": firestore.SERVER_TIMESTAMP
    })
    print(f"Topic {topic_id} created successfully!")
    return topic_id

# Fetch all topics for a subject
def get_topics_by_subject(subject_id):
    topics_ref = db.collection("topics").where("subject_id", "==", subject_id).order_by("unit_index")
    docs = topics_ref.stream()

    print(f"Topics for subject {subject_id}:")
    for doc in docs:
        print(doc.to_dict())

# Update a topic
def update_topic(topic_id, updates):
    topic_ref = db.collection("topics").document(topic_id)
    updates["updated_at"] = firestore.SERVER_TIMESTAMP
    topic_ref.update(updates)
    print(f"Topic {topic_id} updated successfully!")

# Delete a topic
def delete_topic(topic_id):
    topic_ref = db.collection("topics").document(topic_id)
    topic_ref.delete()
    print(f"Topic {topic_id} deleted successfully!")
