from database.topics import create_topic, get_topics_by_subject, update_topic

# Create a new topic
topic_id = create_topic(
    subject_id="de1ec3ee-f899-46d1-a289-b2a2aad924a4", 
    name="Indian National Movement",
    unit_index=1,
    related_topic_ids=[],
    prerequisites=["Basics of British Colonialism"],
    learning_objectives=["Understand the rise of Indian nationalism", "Major events leading to independence"]
)

# Fetch all topics for the subject
get_topics_by_subject("de1ec3ee-f899-46d1-a289-b2a2aad924a4")

# Update a topic (optional)
update_topic(topic_id, {"is_active": False})

# Delete topic (optional)
# delete_topic(topic_id)
