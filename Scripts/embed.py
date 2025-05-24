from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from typing import List, Union

def embed_and_store(
    chunks: Union[List[str], List[dict]],
    persist_dir: str = "embeddings/chromadb/",
    collection_name: str = "api_docs"):

    client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=persist_dir))
    collection = client.get_or_create_collection(collection_name)

    model = SentenceTransformer('all-MiniLM-L6-v2')

    texts = []
    metadatas = []
    ids = []

    for i, chunk in enumerate(chunks):
        if isinstance(chunk, dict):
            texts.append(chunk["text"])
            metadatas.append(chunk.get("metadata", {}))
        else:
            texts.append(chunk)
            metadatas.append({})
        ids.append(f"doc_{i}")

    print(f"Generating embeddings for {len(texts)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True)

    collection.add(documents=texts, embeddings=embeddings, ids=ids, metadatas=metadatas)

    client.persist()
    print(f"Stored {len(texts)} documents in collection '{collection_name}'.")

