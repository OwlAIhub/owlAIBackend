import os
import re
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

FALLBACK_QUIZZES = {
    "teaching aptitude": [
        {
            "question": "Which of the following is a learner-centered method?",
            "A": "Lecture",
            "B": "Demonstration",
            "C": "Group Discussion",
            "D": "Dictation",
            "answer": "C"
        },
        {
            "question": "A teacher uses visual aids to make learning easier. This is related to:",
            "A": "Motivation",
            "B": "Communication",
            "C": "Teaching Aid",
            "D": "Evaluation",
            "answer": "C"
        },
        {
            "question": "Effective teaching includes:",
            "A": "Giving long lectures",
            "B": "Punishing weak students",
            "C": "Making subject easy and interesting",
            "D": "Dictating notes",
            "answer": "C"
        },
        {
            "question": "The best method to study the behavior of a child is:",
            "A": "Observation method",
            "B": "Survey method",
            "C": "Case study method",
            "D": "Experimental method",
            "answer": "A"
        },
        {
            "question": "The most important quality of a good teacher is:",
            "A": "Subject knowledge",
            "B": "Strict discipline",
            "C": "Helping students score high marks",
            "D": "Patience and understanding",
            "answer": "D"
        }
    ]
}

def generate_quiz_questions(topic: str) -> list:
    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a quiz generator assistant for UGC NET Paper 1. "
                    "Your job is to return exactly 5 multiple-choice questions (MCQs) for a given topic. "
                    "Each MCQ should follow this format:\n\n"
                    "Q1: <question text>\n"
                    "A) <option A>\n"
                    "B) <option B>\n"
                    "C) <option C>\n"
                    "D) <option D>\n"
                    "Answer: <A/B/C/D>\n\n"
                    "Do NOT add explanations or headings. Strictly follow this format."
                )
            },
            {"role": "user", "content": f"Topic: {topic}"}
        ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages,
            temperature=0.4
        )
        raw_text = response.choices[0].message.content
        print("[GPT RAW RESPONSE]\n", raw_text)

        parsed = parse_quiz_from_text(raw_text)
        if len(parsed) >= 5:
            return parsed
        else:
            print("⚠️ GPT failed, using fallback.")
            return FALLBACK_QUIZZES.get(topic.strip().lower(), [])
    except Exception as e:
        print("[QuizGen Error]", e)
        return FALLBACK_QUIZZES.get(topic.strip().lower(), [])

def parse_quiz_from_text(text: str) -> list:
    questions = []
    blocks = re.split(r"\n(?=Q\d+:)", text.strip())
    for block in blocks:
        q = {}
        lines = block.strip().splitlines()
        try:
            q["question"] = re.sub(r"^Q\d+:\s*", "", lines[0])
            for line in lines[1:]:
                if line.startswith("A)"):
                    q["A"] = line[3:].strip()
                elif line.startswith("B)"):
                    q["B"] = line[3:].strip()
                elif line.startswith("C)"):
                    q["C"] = line[3:].strip()
                elif line.startswith("D)"):
                    q["D"] = line[3:].strip()
                elif "Answer:" in line:
                    q["answer"] = line.split(":")[-1].strip().upper()
            if all(k in q for k in ["question", "A", "B", "C", "D", "answer"]):
                questions.append(q)
        except Exception as e:
            print(f"[Parse Error] {e}")
            continue
    return questions
