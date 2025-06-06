import re

def detect_language_hint(query: str) -> str:

    if "privacy" in query or "data" in query or "security" in query:
        return "Respond in clear, formal language with precise terminology."
    
    
    hindi = re.search(r'[\u0900-\u097F]', query)
    english = re.search(r'[a-zA-Z]', query)

    if hindi and english:
        return (
            "Respond in Hinglish (mix of Hindi and English). "
            "User is being informal and friendly, so you can match that tone. "
            "Use emojis like 😊, 📚, ✅ where appropriate. Keep it warm and supportive End with an engagement question like: ‘Samjha kya?’, ‘Chalo next karein?’ or can be any thing but engaging"
        )
    elif hindi:
        return (
            "उत्तर सरल और दोस्ताना हिंदी में दें। "
            "व्यवहार में गर्मजोशी रखें और शिक्षार्थी के साथ सहानुभूतिपूर्वक संवाद करें।"
        )
    else:
        return (
            "Respond in polite, supportive English. The user may be casual, so match a friendly tone if needed."
        )
