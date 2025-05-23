from database.motivational_prompts import create_motivational_prompt, get_all_prompts, update_prompt, delete_prompt

# Create
prompt_id = create_motivational_prompt(
    text="You're doing great! Let's keep up the momentum! 💪",
    stage_trigger="exam_preparation",
    user_type_tags=["low_confidence", "night_study"],
    visual_type="emoji",
    delivery_time="21:30",
    target_emotion="encouragement",
    delivery_channel="chatbot"
)

# Read
get_all_prompts()

# Update
update_prompt(prompt_id, {"target_emotion": "motivation"})

# Delete
delete_prompt(prompt_id)

