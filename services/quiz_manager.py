# services/quiz_manager.py

class QuizSession:
    def __init__(self, topic, num_questions=5):
        self.topic = topic
        self.num_questions = num_questions
        self.questions = []
        self.current_index = 0
        self.score = 0
        self.finished = False

    def add_questions(self, questions):
        self.questions = questions[:self.num_questions]

    def get_current_question(self):
        if self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None

    def answer_question(self, user_answer):
        current_q = self.get_current_question()
        if not current_q:
            return None

        correct = current_q["answer"].strip().lower() == user_answer.strip().lower()
        if correct:
            self.score += 1
        self.current_index += 1

        if self.current_index >= self.num_questions:
            self.finished = True

        return correct

    def summary(self):
        return {
            "topic": self.topic,
            "total": self.num_questions,
            "correct": self.score,
            "incorrect": self.num_questions - self.score
        }

    def is_finished(self):
        return self.finished
