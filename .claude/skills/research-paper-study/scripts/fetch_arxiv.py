#!/usr/bin/env python3
"""Fetch paper from arXiv and extract metadata."""
import sys
import re
import requests
import json
from pathlib import Path
import xml.etree.ElementTree as ET

def extract_arxiv_id(input_str):
    """Extract arXiv ID from URL or raw ID."""
    match = re.search(r'(\d{4}\.\d{4,5})', input_str)
    return match.group(1) if match else None

def fetch_arxiv_metadata(arxiv_id):
    """Fetch metadata from arXiv API."""
    api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    response = requests.get(api_url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch metadata: {response.status_code}")
    
    # Parse XML
    root = ET.fromstring(response.content)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    
    entry = root.find('atom:entry', ns)
    if entry is None:
        raise Exception(f"Paper not found: {arxiv_id}")
    
    title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
    authors = [author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)]
    abstract = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
    published = entry.find('atom:published', ns).text[:10]  # YYYY-MM-DD
    
    return {
        'arxiv_id': arxiv_id,
        'title': title,
        'authors': authors,
        'abstract': abstract,
        'published': published,
        'url': f'https://arxiv.org/abs/{arxiv_id}'
    }

def download_pdf(arxiv_id, output_dir="."):
    """Download PDF from arXiv."""
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    output_path = Path(output_dir) / f"{arxiv_id}.pdf"
    
    print(f"Downloading PDF from {pdf_url}...")
    response = requests.get(pdf_url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to download PDF: {response.status_code}")
    
    output_path.write_bytes(response.content)
    return str(output_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: fetch_arxiv.py <arxiv-id-or-url> [output-dir]")
        sys.exit(1)
    
    input_str = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    
    arxiv_id = extract_arxiv_id(input_str)
    if not arxiv_id:
        print(f"❌ Could not extract arXiv ID from: {input_str}")
        sys.exit(1)
    
    try:
        print(f"Fetching metadata for arXiv:{arxiv_id}...")
        metadata = fetch_arxiv_metadata(arxiv_id)
        
        pdf_path = download_pdf(arxiv_id, output_dir)
        metadata['pdf_path'] = pdf_path
        
        # Save metadata as JSON
        metadata_path = Path(output_dir) / f"{arxiv_id}-metadata.json"
        metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))
        
        print(f"\n✅ Fetched: {metadata['title']}")
        print(f"📄 PDF: {pdf_path}")
        print(f"📋 Metadata: {metadata_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
