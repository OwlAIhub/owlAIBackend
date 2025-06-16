from firebase_admin import firestore, initialize_app

# Initialize Firestore
try:
    initialize_app()
except:
    pass

db = firestore.client()

user_id = "kart8798uyhoinc4r"

# 🔍 This is likely the failing query: sessions ordered by start_time
sessions_ref = db.collection("sessions") \
    .where("user_id", "==", user_id) \
    .order_by("start_time", direction=firestore.Query.DESCENDING)

try:
    docs = sessions_ref.stream()
    for doc in docs:
        print(doc.to_dict())
except Exception as e:
    import traceback
    traceback.print_exc()
