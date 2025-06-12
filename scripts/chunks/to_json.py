import re
import json
from pathlib import Path

# === Configuration ===
input_files = [
    "all_chunks.txt",
    "all_chunks2.txt",
    "all_chunks3.txt",
    "all_chunks4.txt"
]

output_file = "parsed_chunks.json"

def clean_chunk(chunk: str) -> dict:
    """Extract title, text, and summary from a chunk."""
    # Remove chunk separators and fake page numbers
    chunk = re.sub(r"--- Chunk \d+ ---", "", chunk)
    chunk = re.sub(r"Page\s*\d+", "", chunk, flags=re.IGNORECASE)

    title_match = re.search(r"Title:\s*(.*)", chunk)
    summary_match = re.search(r"Summary:\s*(.*)", chunk)
    text_match = re.search(r"Text:\s*(.*?)Summary:", chunk, re.DOTALL)

    return {
        "title": title_match.group(1).strip() if title_match else "",
        "text": text_match.group(1).strip() if text_match else "",
        "summary": summary_match.group(1).strip() if summary_match else ""
    }

def main():
    all_chunks = []

    for file_path in input_files:
        path = Path(file_path)
        if not path.exists():
            print(f"File not found: {file_path}")
            continue

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        chunks = re.split(r"--- Chunk \d+ ---", content)
        for raw_chunk in chunks:
            if raw_chunk.strip():
                all_chunks.append(clean_chunk(raw_chunk))

    # Save output JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print(f"Successfully saved {len(all_chunks)} chunks to: {output_file}")

if __name__ == "__main__":
    main()
