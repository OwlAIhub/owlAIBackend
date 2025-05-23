from database.glossary import create_glossary_term, get_glossary_terms, update_glossary_term

# Create a sample glossary term
term_id = create_glossary_term(
    user_id="user_001",
    term="Photosynthesis",
    definition="Photosynthesis is the process by which green plants convert sunlight into chemical energy.",
    subject="Biology",
    unit="Plant Physiology",
    topic="Photosynthesis",
    sub_topic="Light Reaction",
    user_mention_ids=["user_002", "user_003"],
    linked_chat_ids=["chat_123", "chat_456"]
)

# Get glossary terms for user
get_glossary_terms("user_001")

# Update glossary term (optional)
update_glossary_term(term_id, {"definition": "Updated definition of photosynthesis."})
