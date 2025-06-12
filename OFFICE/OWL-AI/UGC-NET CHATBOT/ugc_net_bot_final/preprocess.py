
import fitz
import os
import re
import pandas as pd
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text() for page in doc)
def clean_text(text):
    text = re.sub(r"Page \d+ of \d+", "", text, flags=re.IGNORECASE)
    text = re.sub(r"(UNIVERSITY GRANTS COMMISSION|NET BUREAU|SYLLABUS|Code No\.:.*)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()

def chunk_by_subpoints(text, subject):
    pattern = r"(?=\bUnit\s*[-–]?\s*\w+\s*[:：])|(?=\bUNIT\s*[-–]?\s*\w+\s*[:：])"
    parts = re.split(pattern, text)
    chunks = []
    for part in parts:
        lines = [line.strip() for line in part.strip().split("\n") if line.strip()]
        if not lines:
            continue

        header = lines[0]
        if not re.match(r"(?i)^unit\s*[-–]?\s*\w+\s*[:：]", header):
            continue

        body = " ".join(lines[1:])
        subpoints = re.split(r"(?:\n|•|–|\d+\.\s+|\n\s*\d+\)|\u2022)", body)
        for point in subpoints:
            point = point.strip()
            if len(point) > 30 and not point.isdigit():
                chunks.append({
                    "subject": subject,
                    "unit": header,
                    "content": point
                })

    return chunks

def preprocess_all():
    base_path = os.path.dirname(__file__)
    data_path = os.path.join(base_path, "data")
    subjects = {
        "Education": "Education_English.pdf",
        "Law": "Law_English.pdf",
        "Political Science": "Political_Science_English.pdf"
    }
    all_chunks = []
    for subject, filename in subjects.items():
        file_path = os.path.join(data_path, filename)
        if not os.path.exists(file_path):
            print(f"Skipping missing file: {filename}")
            continue
        text = clean_text(extract_text_from_pdf(file_path))
        chunks = chunk_by_subpoints(text, subject)
        all_chunks.extend(chunks)

    df = pd.DataFrame(all_chunks)
    output_path = os.path.join(data_path, "syllabus_chunks.csv")
    df.to_csv(output_path, index=False)
    print(f"Syllabus chunks saved to: {output_path}")
if __name__ == "__main__":
    preprocess_all()
