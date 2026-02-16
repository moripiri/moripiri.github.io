#!/usr/bin/env python3
"""Compile paper study notes from summary and Q&A discussion."""
import sys
import json
from pathlib import Path
from datetime import datetime

def load_template(lang='en'):
    """Load the appropriate template based on language."""
    template_dir = Path(__file__).parent.parent / 'references'
    template_file = template_dir / f'paper-summary-template-{lang}.md'
    
    if not template_file.exists():
        template_file = template_dir / 'paper-summary-template-en.md'
    
    return template_file.read_text(encoding='utf-8')

def compile_notes(metadata, summary, qa_pairs, insights=None, lang='en'):
    """Compile all components into final markdown."""
    template = load_template(lang)
    
    # Prepare data
    authors_str = ", ".join(metadata.get('authors', ['Unknown']))
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Build Q&A section
    qa_section = ""
    if qa_pairs:
        for q, a in qa_pairs:
            if lang == 'ko':
                qa_section += f"\n### Q: {q}\n**A:** {a}\n"
            else:
                qa_section += f"\n### Q: {q}\n**A:** {a}\n"
    
    # Replace placeholders
    content = template
    replacements = {
        '[Paper Title]': metadata.get('title', 'Untitled'),
        '[Author names]': authors_str,
        '[Publication year]': str(metadata.get('published', 'Unknown')[:4]),
        '[arXiv/DOI URL]': metadata.get('url', ''),
        '[YYYY-MM-DD]': today,
        '[Summary content here]': summary,
        '[Q&A section]': qa_section,
        '[Your thoughts, connections to other work, future directions]': insights or ''
    }
    
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    
    return content

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: compile_study_notes.py <metadata-json> [--lang ko|en] [--output path.md]")
        print("  Then provide summary and Q&A via stdin or interactive prompts")
        sys.exit(1)
    
    metadata_path = Path(sys.argv[1])
    
    # Parse args
    lang = 'en'
    output_path = None
    for i, arg in enumerate(sys.argv):
        if arg == '--lang' and i + 1 < len(sys.argv):
            lang = sys.argv[i + 1]
        if arg == '--output' and i + 1 < len(sys.argv):
            output_path = Path(sys.argv[i + 1])
    
    # Load metadata
    metadata = json.loads(metadata_path.read_text())
    
    # This is a simplified version - in practice, you'd pass summary and Q&A
    # For now, just show the template structure
    print(f"✅ Loaded metadata for: {metadata.get('title', 'Unknown')}")
    print(f"Language: {lang}")
    print(f"Template ready. Use this script with summary and Q&A data to generate notes.")
