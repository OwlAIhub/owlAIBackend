import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    cred = credentials.Certificate("owl-ai-1ef31-firebase-adminsdk-fbsvc-4788ce64d5.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
