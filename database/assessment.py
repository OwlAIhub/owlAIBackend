from database.firebase_connection import db
from firebase_admin import firestore
import uuid

ALLOWED_ASSESSMENT_TYPES = {"MCQ", "Numerical", "Subjective"}
ALLOWED_DIFFICULTY_LEVELS = {"easy", "medium", "hard"}

# Create a new assessment
def create_assessment(subject, unit, assessment_type, difficulty_level, content_ids, duration_minutes, passing_score):
    if assessment_type not in ALLOWED_ASSESSMENT_TYPES:
        raise ValueError(f"Invalid assessment_type. Allowed values are {ALLOWED_ASSESSMENT_TYPES}")
    if difficulty_level not in ALLOWED_DIFFICULTY_LEVELS:
        raise ValueError(f"Invalid difficulty_level. Allowed values are {ALLOWED_DIFFICULTY_LEVELS}")

    assessment_id = str(uuid.uuid4())
    assessment_ref = db.collection("assessments").document(assessment_id)
    assessment_ref.set({
        "assessment_id": assessment_id,
        "subject": subject,
        "unit": unit,
        "type": assessment_type,
        "difficulty_level": difficulty_level,
        "content_ids": content_ids if content_ids else [],
        "duration_minutes": duration_minutes,
        "passing_score": passing_score,
        "created_at": firestore.SERVER_TIMESTAMP,
        "updated_at": firestore.SERVER_TIMESTAMP
    })
    print(f"Assessment {assessment_id} created successfully!")
    return assessment_id

# Get all assessments
def get_all_assessments():
    assessments_ref = db.collection("assessments").order_by("created_at")
    docs = assessments_ref.stream()
    print("Assessments:")
    for doc in docs:
        print(doc.to_dict())

# Update assessment
def update_assessment(assessment_id, updates):
    assessment_ref = db.collection("assessments").document(assessment_id)
    updates["updated_at"] = firestore.SERVER_TIMESTAMP
    assessment_ref.update(updates)
    print(f"Assessment {assessment_id} updated successfully!")

# Delete assessment
def delete_assessment(assessment_id):
    assessment_ref = db.collection("assessments").document(assessment_id)
    assessment_ref.delete()
    print(f"Assessment {assessment_id} deleted successfully!")
