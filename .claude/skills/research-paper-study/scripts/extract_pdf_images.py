#!/usr/bin/env python3
"""Extract images from PDF file."""
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("❌ PyMuPDF not installed. Install with: pip install PyMuPDF")
    sys.exit(1)

def extract_images_from_pdf(pdf_path, output_dir=".", prefix=None):
    """Extract all images from PDF using PyMuPDF."""
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    if prefix is None:
        prefix = pdf_path.stem
    
    print(f"Extracting images from {pdf_path.name}...")
    
    doc = fitz.open(pdf_path)
    image_count = 0
    extracted_images = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images()
        
        if image_list:
            print(f"  Page {page_num + 1}: Found {len(image_list)} image(s)")
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            image_count += 1
            output_filename = f"{prefix}-fig{image_count}.{image_ext}"
            output_path = output_dir / output_filename
            
            output_path.write_bytes(image_bytes)
            
            extracted_images.append({
                'filename': output_filename,
                'path': str(output_path),
                'page': page_num + 1,
                'size': len(image_bytes),
                'format': image_ext
            })
    
    doc.close()
    
    print(f"\n✅ Extracted {image_count} images to {output_dir}")
    return extracted_images

def filter_important_images(images, min_size_kb=20):
    """Filter out small/insignificant images (logos, icons, etc.)."""
    filtered = [img for img in images if img['size'] > min_size_kb * 1024]
    print(f"Filtered: {len(filtered)}/{len(images)} images (>{min_size_kb}KB)")
    return filtered

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: extract_pdf_images.py <pdf-path> [output-dir] [--prefix name] [--min-size-kb N]")
        print("  --prefix: Custom prefix for image filenames (default: PDF filename)")
        print("  --min-size-kb: Minimum image size in KB to extract (default: 20)")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_dir = "."
    prefix = None
    min_size_kb = 20
    
    # Parse optional arguments
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--prefix' and i + 1 < len(sys.argv):
            prefix = sys.argv[i + 1]
            i += 2
        elif arg == '--min-size-kb' and i + 1 < len(sys.argv):
            min_size_kb = int(sys.argv[i + 1])
            i += 2
        elif not arg.startswith('--'):
            output_dir = arg
            i += 1
        else:
            i += 1
    
    try:
        images = extract_images_from_pdf(pdf_path, output_dir, prefix)
        
        if images:
            filtered = filter_important_images(images, min_size_kb)
            
            print("\nExtracted images:")
            for img in filtered:
                print(f"  - {img['filename']} (page {img['page']}, {img['size']//1024}KB)")
        else:
            print("⚠️  No images found in PDF")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
