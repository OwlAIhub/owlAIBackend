
# UGC NET Chatbot (Static Matching)

A command-line chatbot that matches UGC NET questions to static syllabus and Q&A content across 3 subjects: Education, Law, and Political Science.

## Features

- Parses and chunks syllabus PDFs into topic-level content
- Classifies user questions by subject
- Uses TF-IDF + cosine similarity for best match
- Responds using static Q&A (if available), or from syllabus content

## Setup

```bash
pip install -r requirements.txt
```

## Usage

1. Run preprocessing (once):
```bash
python preprocess.py
```

2. Start the chatbot:
```bash
python bot.py
```

## File Structure

- `data/`: PDFs, Q&A JSONs, and syllabus_chunks.csv
- `preprocess.py`: Parses syllabus PDFs
- `match_engine.py`: Matching logic
- `bot.py`: Chat interface
