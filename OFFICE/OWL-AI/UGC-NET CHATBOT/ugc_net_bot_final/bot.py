
from match_engine import match_user_query

def chatbot_loop():
    print("Welcome to the UGC NET Chatbot!")
    print("Ask a question from Education, Law, or Political Science.")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ")
        if question.lower().strip() == "exit":
            print("Bot: Goodbye! and Good Luck!!")
            break
        result = match_user_query(question)
        print(f"\n Subject: {result['matched_subject']}")
        print(f"Source: {result['response_type']}")
        print(f"Answer: {result['response']}")
        print(f"Confidence: {result['confidence']:.2f}\n")
if __name__ == "__main__":
    chatbot_loop()
