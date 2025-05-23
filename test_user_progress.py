from database.user_progress import create_or_update_user_progress, get_user_progress, update_user_progress

# Create a sample user progress record
create_or_update_user_progress(
    user_id="user_001",
    topic_id="topic_123",
    completion_percentage=80.0,
    confidence_level=4,
    repeated_doubt_ids=["doubt_1", "doubt_2"],
    assessment_scores=[{"score": 80, "attempt_date": "2025-04-26"}],
    time_spent_minutes=45
)

# Get user progress
get_user_progress("user_001")

# Update user progress (optional)
update_user_progress("user_001", "topic_123", {"completion_percentage": 90.0, "confidence_level": 5})
