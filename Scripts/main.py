import os
import argparse
from ingest import load_and_parse_docs
from embed import embed_and_store
from retrieve import get_top_k_chunks
from generate import llm_prompt
import sys
def main():
    doc_path = r"E:\Python\Machile Learning\2_Artificial Intelligece\1_API Documentation Q&A Agent\docs"

    if not os.path.exists("embeddings/chromadb") or not os.listdir("embeddings/chromadb") or "--rebuild" in sys.argv:
        print("[*] Ingesting and embedding documentation...")
        chunks = load_and_parse_docs(doc_path)
        if not chunks:
            raise ValueError("[ERROR] No chunks were generated. Check your documents or parsing logic.")
        embed_and_store(chunks)
    
    for chunk in chunks:
        print(f"\n[Chunk ID: {chunk['chunk_id']}]")
        print(f"Source: {chunk['source']}")
        print(chunk['text'][:300], '...' if len(chunk['text']) > 300 else '')

    print("\nAsk a question about the API (type 'q' to quit):")
    while True:
        question = input("\n>> ")
        if question.lower() == "q":
            break
        context = get_top_k_chunks(question)
        answer = llm_prompt(question, context["documents"])
        print("\n🧠 Answer:")
        print(answer)
        print("\n---")

if __name__ == "__main__":
    main()
