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
    return {
        "documents": results.get("documents", [[]])[0],
        "metadatas": results.get("metadatas", [[]])[0],
        "distances": results.get("distances", [[]])[0],
    }
