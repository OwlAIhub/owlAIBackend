from database.subjects import create_subject, get_subjects, update_subject

# Create a new subject
subject_id = create_subject(
    name="Political Science",
    stream_type="humanities",
    syllabus_version="2025",
    applicable_exam_ids=["ugc_net_political_science", "state_civil_services"],
    is_active=True
)

# Fetch all subjects
get_subjects()

# Update subject (optional)
update_subject(subject_id, {"is_active": False})

# Delete subject (optional)
# delete_subject(subject_id)
