from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
from typing import List, Union

def embed_and_store(chunks: Union[List[str], List[dict]], persist_dir: str = "embeddings/chromadb/", collection_name: str = "api_docs"):
    client = PersistentClient(path=persist_dir)
    collection = client.get_or_create_collection(collection_name)
    
    model = SentenceTransformer('all-MiniLM-L6-v2')

    texts = []
    metadatas = []
    ids = []

    for i, chunk in enumerate(chunks):
        if isinstance(chunk, dict):
            texts.append(chunk["text"])
            metadatas.append({
                "source": chunk.get("source", "unknown"),
                "chunk_id": chunk.get("chunk_id", str(i))
            })
        else:
            texts.append(chunk)
            metadatas.append({})
        ids.append(f"doc_{i}")

    print(f"Generating embeddings for {len(texts)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True)

    collection.add(documents=texts, embeddings=embeddings, ids=ids, metadatas=metadatas)

    print(f"Stored {len(texts)} documents in collection '{collection_name}' at '{persist_dir}'")
