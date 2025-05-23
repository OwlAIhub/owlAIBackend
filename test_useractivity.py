from database.user_activity import create_user_activity, get_all_user_activities, update_user_activity, delete_user_activity

# Create
activity_id = create_user_activity(
    session_id="session_001",
    user_id="user_001",
    question_log="What is Constructivism?; Give Bloom's Taxonomy;",
    confusion_flag=True,
    auto_generated_tags=["educational_theory", "bloom"],
    language_pattern="hinglish",
    session_duration=25
)

# Read
get_all_user_activities()

# Update
update_user_activity(activity_id, {"session_duration": 30, "language_pattern": "english"})

# Delete
delete_user_activity(activity_id)
