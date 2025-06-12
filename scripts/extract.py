from pdf2image import convert_from_path
import pytesseract
import os

# Config
PDF_DIR = "pdf"              # Folder where all your PDFs are
OUTPUT_DIR = "ocr_texts"     # Folder where combined OCR text files will be saved
DPI = 300

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Get list of all PDF files in the input directory
pdf_files = [f for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")]

for pdf_file in pdf_files:
    pdf_path = os.path.join(PDF_DIR, pdf_file)
    base_name = os.path.splitext(pdf_file)[0]
    print(f"\n📘 Processing PDF: {pdf_file}")

    try:
        images = convert_from_path(pdf_path, dpi=DPI)
    except Exception as e:
        print(f"❌ Failed to convert {pdf_file}: {e}")
        continue

    full_text = ""  # Initialize text accumulator

    for i, img in enumerate(images):
        page_number = i + 1
        print(f"   → OCR page {page_number}...")
        text = pytesseract.image_to_string(img, lang='eng')
        full_text += f"\n\n=== Page {page_number} ===\n{text}"

    # Save combined OCR text to a single file
    output_file_name = f"{base_name}.txt"
    output_path = os.path.join(OUTPUT_DIR, output_file_name)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_text)

print("\n✅ OCR complete for all PDFs. Combined text saved per PDF.")
