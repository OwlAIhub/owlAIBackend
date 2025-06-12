import os
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

base_path = os.path.dirname(__file__)
data_path = os.path.join(base_path, "data")
syllabus_df = pd.read_csv(os.path.join(data_path, "syllabus_chunks.csv"))

def load_qa(subject):
    path = os.path.join(data_path, f"{subject.lower().replace(' ', '_')}_qa.json")
    if os.path.exists(path):
        with open(path) as f:
            return pd.DataFrame(json.load(f))
    return pd.DataFrame(columns=["question", "answer"])

qa_data = {
    "Education": load_qa("Education"),
    "Law": load_qa("Law"),
    "Political Science": load_qa("Political Science")
}

vectorizer = TfidfVectorizer(stop_words="english")
syllabus_tfidf = vectorizer.fit_transform(syllabus_df["content"])

def match_user_query(query):
    for subject, df in qa_data.items():
        if not df.empty:
            tfidf = TfidfVectorizer(stop_words="english")
            tfidf_matrix = tfidf.fit_transform(df["question"])
            query_vec = tfidf.transform([query])
            sim_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
            best_idx = np.argmax(sim_scores)
            if sim_scores[best_idx] > 0.5:
                return {
                    "matched_subject": subject,
                    "response_type": "Sample Q&A",
                    "response": df.iloc[best_idx]["answer"],
                    "confidence": float(sim_scores[best_idx])
                }

    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, syllabus_tfidf).flatten()
    top_idx = np.argmax(similarities)

    return {
        "matched_subject": syllabus_df.iloc[top_idx]["subject"],
        "response_type": "Syllabus",
        "response": syllabus_df.iloc[top_idx]["content"],
        "confidence": float(similarities[top_idx])
    }
