# from bs4 import BeautifulSoup
# import os

# def load_and_parse_docs(doc_path: str) -> list[str]:
#     if doc_path.endswith('.html'):
#         with open(doc_path, 'r', encoding='utf-8') as f:
#             soup = BeautifulSoup(f, 'html.parser')
#             text = soup.get_text()
#     else:
#         with open(doc_path, 'r', encoding='utf-8') as f:
#             text = f.read()
#     return [chunk.strip() for chunk in text.split('\n\n') if len(chunk.strip()) > 50]


import os
from bs4 import BeautifulSoup

def load_and_parse_docs(doc_dir: str, min_chunk_length: int = 50) -> list[dict]:
    supported_exts = ('.html', '.md', '.txt')
    chunks = []

    for root, _, files in os.walk(doc_dir):
        for file in files:
            if file.endswith(supported_exts):
                file_path = os.path.join(root, file)
                ext = os.path.splitext(file)[1]

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if ext == '.html':
                        soup = BeautifulSoup(content, 'html.parser')
                        text = soup.get_text(separator="\n")
                    else:
                        text = content
                raw_chunks = [c.strip() for c in text.split('\n\n') if len(c.strip()) >= min_chunk_length]
                for i, chunk in enumerate(raw_chunks):
                    chunks.append({
                        "text": chunk,
                        "source": file_path,
                        "chunk_id": f"{file}_{i}"
                    })

    return chunks
