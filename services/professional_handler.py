PROFESSIONAL_RESPONSES = {
    "source_query": {
        "en": "📚 My knowledge comes from curated UGC NET resources:\n"
               "- Official UGC/NET syllabus documents\n"
               "- Standard reference books (e.g., Trueman's, Arihant)\n"
               "- Previous year question papers (2015-2023)\n"
               "- Verified educational content from NTA-approved sources\n\n"
               "For specific references, ask about any topic!",
        "hi": "📚 मेरा ज्ञान यूजीसी नेट के चयनित संसाधनों से आता है:\n"
              "- आधिकारिक यूजीसी/नेट पाठ्यक्रम\n"
              "- मानक संदर्भ पुस्तकें (जैसे ट्रूमैन, अरिहंत)\n"
              "- पिछले वर्षों के प्रश्न पत्र (2015-2023)\n"
              "- एनटीए-अनुमोदित शैक्षिक सामग्री\n\n"
              "विशिष्ट संदर्भों के लिए किसी भी विषय के बारे में पूछें!"
    },
    "privacy_query": {
        "en": "🔒 Your privacy is paramount:\n"
               "- Chat data is encrypted and stored securely\n"
               "- Personal info is never shared/sold\n",
               
        "hi": "🔒 आपकी गोपनीयता सर्वोपरि है:\n"
              "- चैट डेटा एन्क्रिप्टेड और सुरक्षित रूप से संग्रहीत है\n"
              "- व्यक्तिगत जानकारी कभी साझा/बेची नहीं जाती\n"
              
    },
    "creator_query": {
        "en": "👨‍💻 I was developed by:\n"
               "- Owl Education Technologies Pvt Ltd\n"
               "- Specializing in AI-powered UGC NET prep\n"
               "- Founded by IIT alumni & NET qualifiers\n"
               "Our mission: Make quality education accessible!",
        "hi": "👨‍💻 मुझे विकसित किया गया था:\n"
              "- उल एजुकेशन टेक्नोलॉजीज प्राइवेट लिमिटेड द्वारा\n"
              "- एआई-संचालित यूजीसी नेट तैयारी में विशेषज्ञ\n"
              "- आईआईटी पूर्व छात्रों और नेट योग्यता धारकों द्वारा स्थापित\n"
              "हमारा मिशन: गुणवत्तापूर्ण शिक्षा सुलभ बनाना!"
    }
}

def handle_professional_query(intent_type: str, query: str) -> str:
    from services.language_detect import detect_language_hint
    lang = detect_language_hint(query)
    
    # Simple language mapping
    if lang == "hi": 
        lang_key = "hi"
    elif lang == "hinglish":
        lang_key = "en"  
    else:
        lang_key = "en"
    
    response = PROFESSIONAL_RESPONSES[intent_type].get(lang_key, PROFESSIONAL_RESPONSES[intent_type]["en"])
    
    # Add Hinglish flavor if needed
    if lang == "hinglish":
        return response.replace("My", "Mera").replace("I was", "Main").replace("Our", "Hamara") + " 😊"
    
    return response