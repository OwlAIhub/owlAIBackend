from database.firebase_connection import db
from firebase_admin import firestore
import uuid

ALLOWED_STAGE_TRIGGERS = {"onboarding", "exam_preparation", "post_exam"}
ALLOWED_VISUAL_TYPES = {"emoji", "owl_doodle"}
ALLOWED_DELIVERY_CHANNELS = {"chatbot", "email", "push"}

# Create a motivational prompt
def create_motivational_prompt(text, stage_trigger, user_type_tags, visual_type, delivery_time, target_emotion, delivery_channel):
    if stage_trigger not in ALLOWED_STAGE_TRIGGERS:
        raise ValueError(f"Invalid stage_trigger. Allowed values are {ALLOWED_STAGE_TRIGGERS}")
    if visual_type not in ALLOWED_VISUAL_TYPES:
        raise ValueError(f"Invalid visual_type. Allowed values are {ALLOWED_VISUAL_TYPES}")
    if delivery_channel not in ALLOWED_DELIVERY_CHANNELS:
        raise ValueError(f"Invalid delivery_channel. Allowed values are {ALLOWED_DELIVERY_CHANNELS}")

    prompt_id = str(uuid.uuid4())
    prompt_ref = db.collection("motivational_prompts").document(prompt_id)
    prompt_ref.set({
        "prompt_id": prompt_id,
        "text": text,
        "stage_trigger": stage_trigger,
        "user_type_tags": user_type_tags if user_type_tags else [],
        "visual_type": visual_type,
        "delivery_time": delivery_time,
        "target_emotion": target_emotion,
        "delivery_channel": delivery_channel,
        "created_at": firestore.SERVER_TIMESTAMP,
        "updated_at": firestore.SERVER_TIMESTAMP
    })
    print(f"Motivational Prompt {prompt_id} created successfully!")
    return prompt_id

# Fetch all prompts
def get_all_prompts():
    prompts_ref = db.collection("motivational_prompts").order_by("created_at")
    docs = prompts_ref.stream()
    print("Motivational Prompts:")
    for doc in docs:
        print(doc.to_dict())

# Update a prompt
def update_prompt(prompt_id, updates):
    prompt_ref = db.collection("motivational_prompts").document(prompt_id)
    updates["updated_at"] = firestore.SERVER_TIMESTAMP
    prompt_ref.update(updates)
    print(f"Motivational Prompt {prompt_id} updated successfully!")

# Delete a prompt
def delete_prompt(prompt_id):
    prompt_ref = db.collection("motivational_prompts").document(prompt_id)
    prompt_ref.delete()
    print(f"Motivational Prompt {prompt_id} deleted successfully!")
