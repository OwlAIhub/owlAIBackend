from database.firebase_connection import db
from firebase_admin import firestore
import uuid

ALLOWED_TONE_TYPES = {"formal", "informal", "encouraging"}

# Create a language variant
def create_language_variant(subject, unit, topic, original_text, translated_text, language, tone_type):
    if tone_type not in ALLOWED_TONE_TYPES:
        raise ValueError(f"Invalid tone_type. Allowed values are {ALLOWED_TONE_TYPES}")

    variant_id = str(uuid.uuid4())
    variant_ref = db.collection("language_variants").document(variant_id)
    variant_ref.set({
        "variant_id": variant_id,
        "subject": subject,
        "unit": unit,
        "topic": topic,
        "original_text": original_text,
        "translated_text": translated_text,
        "language": language,
        "tone_type": tone_type,
        "created_at": firestore.SERVER_TIMESTAMP,
        "updated_at": firestore.SERVER_TIMESTAMP
    })
    print(f"Language Variant {variant_id} created successfully!")
    return variant_id

# Get all variants
def get_all_language_variants():
    variants_ref = db.collection("language_variants").order_by("created_at")
    docs = variants_ref.stream()
    print("Language Variants:")
    for doc in docs:
        print(doc.to_dict())

# Update a variant
def update_language_variant(variant_id, updates):
    variant_ref = db.collection("language_variants").document(variant_id)
    updates["updated_at"] = firestore.SERVER_TIMESTAMP
    variant_ref.update(updates)
    print(f"Language Variant {variant_id} updated successfully!")

# Delete a variant
def delete_language_variant(variant_id):
    variant_ref = db.collection("language_variants").document(variant_id)
    variant_ref.delete()
    print(f"Language Variant {variant_id} deleted successfully!")
