from database.assessment import create_assessment, get_all_assessments, update_assessment, delete_assessment

# Create
assessment_id = create_assessment(
    subject="Education",
    unit="Unit 5",
    assessment_type="MCQ",
    difficulty_level="medium",
    content_ids=["content_123", "content_456"],
    duration_minutes=30,
    passing_score=60
)

# Read
get_all_assessments()

# Update
update_assessment(assessment_id, {"duration_minutes": 40, "passing_score": 65})

# Delete
delete_assessment(assessment_id)
