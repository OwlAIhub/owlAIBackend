from database.firebase_connection import db
from firebase_admin import firestore
import uuid

ALLOWED_CONDITION_TYPES = {"streak", "completion", "time-based"}
ALLOWED_AB_TEST_STATUS = {"active", "variant_a", "variant_b"}

# Create a new motivational trigger
def create_motivational_trigger(condition_type, trigger_value, message_template, visual_emoji, audience_type, trigger_priority, ab_test_status="active"):
    if condition_type not in ALLOWED_CONDITION_TYPES:
        raise ValueError(f"Invalid condition_type. Allowed values are {ALLOWED_CONDITION_TYPES}")
    if ab_test_status not in ALLOWED_AB_TEST_STATUS:
        raise ValueError(f"Invalid ab_test_status. Allowed values are {ALLOWED_AB_TEST_STATUS}")

    trigger_id = str(uuid.uuid4())
    trigger_ref = db.collection("motivational_triggers").document(trigger_id)
    trigger_ref.set({
        "id": trigger_id,
        "condition_type": condition_type,
        "trigger_value": trigger_value,
        "message_template": message_template,
        "visual_emoji": visual_emoji,
        "audience_type": audience_type,
        "trigger_priority": trigger_priority,
        "ab_test_status": ab_test_status,
        "created_at": firestore.SERVER_TIMESTAMP,
        "updated_at": firestore.SERVER_TIMESTAMP
    })
    print(f"Motivational Trigger {trigger_id} created successfully!")
    return trigger_id

# Get all motivational triggers
def get_all_motivational_triggers():
    triggers_ref = db.collection("motivational_triggers").order_by("created_at")
    docs = triggers_ref.stream()
    print("Motivational Triggers:")
    for doc in docs:
        print(doc.to_dict())

# Update trigger
def update_motivational_trigger(trigger_id, updates):
    trigger_ref = db.collection("motivational_triggers").document(trigger_id)
    updates["updated_at"] = firestore.SERVER_TIMESTAMP
    trigger_ref.update(updates)
    print(f"Motivational Trigger {trigger_id} updated successfully!")

# Delete trigger
def delete_motivational_trigger(trigger_id):
    trigger_ref = db.collection("motivational_triggers").document(trigger_id)
    trigger_ref.delete()
    print(f"Motivational Trigger {trigger_id} deleted successfully!")
