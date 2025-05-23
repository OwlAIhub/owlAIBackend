from database.sessions import create_session, update_session, end_session

# Step 1: Create a session
session_id = create_session(
    user_id="user_001",
    session_type="practice",
    device_type="web",
    ip_address="192.168.1.10",
    question_ids=["q1", "q2", "q3"]
)

# Step 2: Update session (optional)
update_session(session_id, {"session_type": "test"})

# Step 3: End session (optional)
end_session(session_id)
