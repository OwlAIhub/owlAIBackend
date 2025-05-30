# test_llm.py

from services.llm import get_response_from_llm

prompt = "Explain how AI works in a few words"
response = get_response_from_llm(prompt)

print("\n🧠 Gemini Response:\n")
print(response)
