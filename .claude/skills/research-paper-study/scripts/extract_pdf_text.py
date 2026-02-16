#!/usr/bin/env python3
"""Extract text from PDF file."""
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("❌ pdfplumber not installed. Install with: pip install pdfplumber")
    sys.exit(1)

def extract_text_from_pdf(pdf_path, output_path=None):
    """Extract text from PDF using pdfplumber."""
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    print(f"Extracting text from {pdf_path.name}...")
    
    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"Total pages: {total_pages}")
        
        for i, page in enumerate(pdf.pages, 1):
            if i % 5 == 0:
                print(f"  Processing page {i}/{total_pages}...")
            text_parts.append(page.extract_text())
    
    full_text = "\n\n".join(filter(None, text_parts))
    
    if output_path:
        output_path = Path(output_path)
        output_path.write_text(full_text, encoding='utf-8')
        print(f"✅ Extracted {len(full_text)} characters to {output_path}")
        return str(output_path)
    else:
        return full_text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: extract_pdf_text.py <pdf-path> [output-txt-path]")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        result = extract_text_from_pdf(pdf_path, output_path)
        if not output_path:
            print(result)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
