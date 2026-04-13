import chromadb
from chromadb.config import Settings
import os

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")

def get_client():
    """Get ChromaDB client with persistence."""
    return chromadb.Client(Settings(
        persist_directory=CHROMA_PERSIST_DIR,
        anonymized_telemetry=False
    ))

def get_collection(client, collection_name="documents"):
    """Get or create a collection for document embeddings."""
    return client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )
