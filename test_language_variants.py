from database.language_variants import create_language_variant, get_all_language_variants, update_language_variant, delete_language_variant

# Create
variant_id = create_language_variant(
    subject="Education",
    unit="Unit 2",
    topic="Bloom's Taxonomy",
    original_text="Bloom's taxonomy helps structure learning outcomes.",
    translated_text="ब्लूम की टैक्सोनॉमी सीखने के परिणामों को संरचित करने में मदद करती है।",
    language="Hindi",
    tone_type="encouraging"
)

# Read
get_all_language_variants()

# Update
update_language_variant(variant_id, {"tone_type": "formal"})

# Delete
delete_language_variant(variant_id)
