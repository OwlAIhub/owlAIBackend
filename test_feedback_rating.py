from database.feedback_rating import create_feedback, get_feedback_by_chat, update_feedback

# Create feedback rating
feedback_id = create_feedback(
    chat_id="chat_123", 
    user_id="user_001", 
    usefulness_score=4, 
    content_quality_score=5, 
    flagged_reason="inaccurate", 
    remarks="Answer missed key points."
)

# Fetch feedbacks for a chat
get_feedback_by_chat("chat_123")

# Update feedback (optional)
update_feedback(feedback_id, {"remarks": "Updated remarks after review."})

