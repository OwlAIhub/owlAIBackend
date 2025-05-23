from database.motivational_triggers import create_motivational_trigger, get_all_motivational_triggers, update_motivational_trigger, delete_motivational_trigger

# Create
trigger_id = create_motivational_trigger(
    condition_type="streak",
    trigger_value=3,
    message_template="You've maintained a 3-day streak! 🔥 Keep going!",
    visual_emoji="🔥",
    audience_type="all_users",
    trigger_priority=1,
    ab_test_status="active"
)

# Read
get_all_motivational_triggers()

# Update
update_motivational_trigger(trigger_id, {"trigger_priority": 2})

# Delete
delete_motivational_trigger(trigger_id)
