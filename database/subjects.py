from database.firebase_connection import db
from firebase_admin import firestore
import uuid

# Create a new subject
def create_subject(name, stream_type, syllabus_version, applicable_exam_ids=None, is_active=True):
    subject_id = str(uuid.uuid4())
    subject_ref = db.collection("subjects").document(subject_id)
    subject_ref.set({
        "id": subject_id,
        "name": name,
        "stream_type": stream_type,
        "syllabus_version": syllabus_version,
        "applicable_exam_ids": applicable_exam_ids if applicable_exam_ids else [],
        "is_active": is_active,
        "created_at": firestore.SERVER_TIMESTAMP,
        "updated_at": firestore.SERVER_TIMESTAMP
    })
    print(f"Subject {subject_id} created successfully!")
    return subject_id

# Fetch all subjects
def get_subjects():
    subjects_ref = db.collection("subjects").order_by("created_at")
    docs = subjects_ref.stream()

    print("Subjects List:")
    for doc in docs:
        print(doc.to_dict())

# Update subject
def update_subject(subject_id, updates):
    subject_ref = db.collection("subjects").document(subject_id)
    updates["updated_at"] = firestore.SERVER_TIMESTAMP
    subject_ref.update(updates)
    print(f"Subject {subject_id} updated successfully!")

# Delete subject
def delete_subject(subject_id):
    subject_ref = db.collection("subjects").document(subject_id)
    subject_ref.delete()
    print(f"Subject {subject_id} deleted successfully!")
