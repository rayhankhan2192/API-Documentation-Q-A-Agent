import os
from bs4 import BeautifulSoup
import fitz
from typing import List, Dict

def extract_pdf_text(path: str) -> str:
    doc = fitz.open(path)
    return "\n".join(page.get_text() for page in doc)

def load_and_parse_docs(doc_dir: str, min_chunk_length: int = 50) -> List[Dict]:
    supported_exts = ('.html', '.md', '.txt', '.pdf')
    chunks = []

    for root, _, files in os.walk(doc_dir):
        for file in files:
            if file.endswith(supported_exts):
                file_path = os.path.join(root, file)
                ext = os.path.splitext(file)[1]

                if ext == '.pdf':
                    text = extract_pdf_text(file_path)
                else:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        if ext == '.html':
                            soup = BeautifulSoup(f.read(), 'html.parser')
                            text = soup.get_text(separator="\n")
                        else:
                            text = f.read()

                raw_chunks = [c.strip() for c in text.split('\n\n') if len(c.strip()) >= min_chunk_length]
                for i, chunk in enumerate(raw_chunks):
                    chunks.append({
                        "text": chunk,
                        "source": file_path,
                        "chunk_id": f"{file}_{i}"
                    })
    return chunks
