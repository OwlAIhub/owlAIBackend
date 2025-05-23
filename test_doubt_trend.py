from database.doubt_trend import create_doubt_trend, get_all_doubt_trends, update_doubt_trend, delete_doubt_trend

# Create
feed_id = create_doubt_trend(
    title="Top Confusing Theories - Unit 3",
    subject="Education",
    unit="Unit 3",
    topic="Learning Theories",
    sub_topic="Constructivism",
    question_ids=["q1", "q2", "q3"],
    frequency_count=[10, 8, 12],
    trending_score=91,
    date_range="2025-04-20 to 2025-04-27",
    geo_location="Uttar Pradesh"
)

# Read
get_all_doubt_trends()

# Update
update_doubt_trend(feed_id, {"trending_score": 95})

# Delete
delete_doubt_trend(feed_id)
