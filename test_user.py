from database.user import create_user

user_id = create_user(
    name="Aryan Sharma",
    email="aryan@example.com",
    mobile_number="9876543210",
    gender="Male",
    age_group="18-24",
    region="North",
    exam_ids=["ugc_net_education", "ugc_net_law"],
    referral_code="REF123"
)


