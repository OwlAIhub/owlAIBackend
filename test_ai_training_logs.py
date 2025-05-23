from database.ai_training_logs import create_ai_training_log, get_all_ai_training_logs, update_ai_training_log, delete_ai_training_log

# Create
log_id = create_ai_training_log(
    prompt_text="Explain Bloom's Taxonomy in simple terms.",
    ai_response="Bloom's Taxonomy is a classification of thinking according to six levels...",
    feedback_score=2,
    corrected_by_admin="Rephrased to include examples.",
    training_tag="accuracy",
    model_version="v1.2.0"
)

# Read
get_all_ai_training_logs()

# Update
update_ai_training_log(log_id, {"feedback_score": 4, "training_tag": "tone"})

# Delete
delete_ai_training_log(log_id)
