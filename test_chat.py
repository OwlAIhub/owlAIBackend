from database.chats import save_chat, get_chat_history

# Save a sample chat
chat_id = save_chat(
    user_id="user_001",
    subject="History",
    unit="Medieval India",
    topic="Bhakti Movement",
    sub_topic="Saint Poets",
    question_text="What is Bhakti Movement?",
    response_text="Bhakti Movement was a devotional trend that emerged in medieval India...",
    source_ref_type="syllabus",
    source_ref_id="content_123",
    media_type="text",
    media_url=None,
    topic_tags=["bhakti", "medieval", "history"],
    feedback_rating=4
)

# Get chat history
get_chat_history("user_001")

# Delete chat (optional)
# delete_chat(chat_id)
