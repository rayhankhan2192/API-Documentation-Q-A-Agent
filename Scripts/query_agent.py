import ollama
from typing import List
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb import PersistentClient
from chromadb.config import Settings

def get_top_k_chunks(
    question: str,
    k: int = 5,
    persist_dir: str = "embeddings/chromadb/",
    collection_name: str = "api_docs"):

    client = PersistentClient(path=persist_dir)
    collection = client.get_collection(collection_name)

    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode([question], show_progress_bar=False)[0]

    results = collection.query(query_embeddings=[query_embedding], n_results=k)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    combined = [
        {"text": doc, "source": meta.get("source", "N/A")}
        for doc, meta in zip(documents, metadatas)
    ]

    return {
        "documents": combined,
        "distances": results.get("distances", [[]])[0],
    }



def llm_prompt(question: str, context_chunks: List[str]) -> str:
    try:
        context = "\n\n".join(context_chunks)
        prompt = f"""Answer the following question using only the context provided below.
        If the context is insufficient, say exactly: "I don't have enough information to answer."
        Do NOT add any further information or explanation.

        Context:
        {context}

        Question: {question}
        Answer:"""

        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}],
        )
        answer = response['message']['content'].strip()
        fallback = "I don't have enough information to answer."
        if fallback in answer:
            return fallback

        return answer

    except Exception as e:
        return f"Failed to get response: {e}"