import os
import re
from pathlib import Path
from langchain.chat_models import ChatOpenAI

# === Step 0: Set your OpenAI API Key directly ===
os.environ["OPENAI_API_KEY"] = "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"

# === Configuration ===
FOLDER_PATH = "ocr_texts"
TARGET_CHARS = 2000
OVERLAP_CHARS = 200

# === Step 1: Read & Merge .txt Files ===
def read_and_merge_texts(folder_path):
    files = sorted(Path(folder_path).glob("*.txt"))
    all_text = ""
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            all_text += f.read() + "\n\n"
    return all_text

# === Step 2: Clean Text ===
def clean_text(text, detect_headers=True):
    """
    Cleans OCR text while avoiding accidental deletion of valid content.
    - Removes headers/footers only if they appear consistently across pages.
    - Preserves genuine content with important keywords like 'education', 'chapter', etc.
    """

    lines = text.split("\n")
    cleaned_lines = []
    candidate_headers = []
    candidate_footers = []

    # Track first/last line of each "page" (simulate page detection by blank lines)
    block = []
    for line in lines:
        line = line.strip()
        if not line:
            if block:
                candidate_headers.append(block[0].lower())
                candidate_footers.append(block[-1].lower())
                block = []
            continue
        block.append(line)

    # If we captured enough pages, find repeating headers/footers
    from collections import Counter

    header_counts = Counter(candidate_headers)
    footer_counts = Counter(candidate_footers)

    # Choose headers/footers that appear on most pages (e.g., > 30%)
    header_cutoff = max(2, int(len(candidate_headers) * 0.3))
    common_headers = {h for h, c in header_counts.items() if c >= header_cutoff}
    common_footers = {f for f, c in footer_counts.items() if c >= header_cutoff}

    # === Actual filtering ===
    for line in lines:
        line_clean = line.strip()

        # Skip empty
        if not line_clean:
            continue

        # Skip very short/noisy lines
        if len(line_clean) < 5 and not line_clean.endswith("."):
            continue

        # Remove if it matches known header/footer pattern
        if detect_headers:
            lc_line = line_clean.lower()
            if lc_line in common_headers or lc_line in common_footers:
                continue

        cleaned_lines.append(line_clean)

    text_out = " ".join(cleaned_lines)
    text_out = re.sub(r'\s+', ' ', text_out).strip()
    return text_out

# === Step 3: Chunk with Overlap ===
def chunk_text_paragraph_based(text, target_chars=2000, overlap_chars=200):
    """
    Split text by paragraph boundaries with overlap, avoiding mid-sentence splits.
    """
    paragraphs = re.split(r'\n\s*\n|\.\s', text)  # Split by paragraph or full stop
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        if len(current_chunk) + len(para) <= target_chars:
            current_chunk += para + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    # Add overlap (optional)
    final_chunks = []
    for i in range(len(chunks)):
        chunk = chunks[i]
        if i > 0:
            overlap = chunks[i - 1][-overlap_chars:]  # last X chars from previous
            chunk = overlap + " " + chunk
        final_chunks.append(chunk.strip())

    return final_chunks


# === Step 4: GPT-4 Summary ===
llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.2)

def generate_summary(text):
    prompt = f"Summarize this in one sentence:\n\n{text}"
    return llm.invoke(prompt)

def generate_title(text):
    prompt = f"Give a short and clear title for this text:\n\n{text}"
    return llm.invoke(prompt)

def get_clean_response(llm, text, mode="summary"):
    if mode == "summary":
        prompt = f"Summarize this in one sentence:\n\n{text}"
    elif mode == "title":
        prompt = f"Give a short and clear title for this text:\n\n{text}"
    else:
        raise ValueError("Invalid mode. Use 'summary' or 'title'.")

    response = llm.invoke(prompt)
    return response.content if hasattr(response, "content") else response



def save_all_chunks_to_single_txt(chunks, titles, summaries, output_file="all_chunks.txt"):
    with open(output_file, "w", encoding="utf-8") as f:
        for i, (chunk, title, summary) in enumerate(zip(chunks, titles, summaries), start=1):
            f.write(f"--- Chunk {i} ---\n")
            f.write(f"Title: {title}\n\n")
            f.write("Text:\n")
            f.write(chunk + "\n\n")
            f.write("Summary:\n")
            f.write(summary + "\n\n")
            f.write("="*80 + "\n\n")



# === Step 5: Run Agentic Chunking ===
def run_agentic_chunking():
    raw_text = read_and_merge_texts(FOLDER_PATH)
    cleaned_text = clean_text(raw_text)
    chunks = chunk_text_paragraph_based(cleaned_text, TARGET_CHARS, OVERLAP_CHARS)

    all_titles = []
    all_summaries = []

    for i, chunk in enumerate(chunks, start=1):
        summary = get_clean_response(llm, chunk, mode="summary")
        title = get_clean_response(llm, chunk, mode="title")

        all_titles.append(title)
        all_summaries.append(summary)

        print(f"\n--- Chunk {i} ---")
        print(f"Title: {title}")
        print(f"Text:\n{chunk}\n")
        print(f"Summary: {summary}")

    # Save to single .txt file
    save_all_chunks_to_single_txt(chunks, all_titles, all_summaries)



# === Execute ===
if __name__ == "__main__":
    run_agentic_chunking()
