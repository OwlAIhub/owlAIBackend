from database.firebase_connection import db
from firebase_admin import firestore
import uuid

# Create a new doubt trend entry
def create_doubt_trend(title, subject, unit, topic, sub_topic, question_ids=None, frequency_count=None, trending_score=0, date_range=None, geo_location=None):
    feed_id = str(uuid.uuid4())
    trend_ref = db.collection("doubt_trends").document(feed_id)
    trend_ref.set({
        "feed_id": feed_id,
        "title": title,
        "subject": subject,
        "unit": unit,
        "topic": topic,
        "sub_topic": sub_topic,
        "question_ids": question_ids if question_ids else [],
        "frequency_count": frequency_count if frequency_count else [],
        "trending_score": trending_score,
        "date_range": date_range if date_range else None,
        "geo_location": geo_location if geo_location else None,
        "created_at": firestore.SERVER_TIMESTAMP,
        "updated_at": firestore.SERVER_TIMESTAMP
    })
    print(f"Doubt Trend {feed_id} created successfully!")
    return feed_id

# Get all doubt trends
def get_all_doubt_trends():
    trends_ref = db.collection("doubt_trends").order_by("created_at")
    docs = trends_ref.stream()
    print("Doubt Trends:")
    for doc in docs:
        print(doc.to_dict())

# Update doubt trend
def update_doubt_trend(feed_id, updates):
    trend_ref = db.collection("doubt_trends").document(feed_id)
    updates["updated_at"] = firestore.SERVER_TIMESTAMP
    trend_ref.update(updates)
    print(f"Doubt Trend {feed_id} updated successfully!")

# Delete doubt trend
def delete_doubt_trend(feed_id):
    trend_ref = db.collection("doubt_trends").document(feed_id)
    trend_ref.delete()
    print(f"Doubt Trend {feed_id} deleted successfully!")
