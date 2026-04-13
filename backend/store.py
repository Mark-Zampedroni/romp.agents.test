from .database import get_client, get_collection
from .embeddings import EmbeddingService
from .parser import DocumentParser
import os
import uuid
from typing import List, Tuple

class DocumentStore:
    """Manage document storage and retrieval with embeddings."""
    
    def __init__(self):
        self.client = get_client()
        self.collection = get_collection(self.client)
        self.embedding_service = EmbeddingService()
    
    def add_document(self, filename: str, content: str, chunk_size: int = 500, overlap: int = 50) -> dict:
        """Add a document to the store."""
        # Chunk the document
        chunks = self.embedding_service.chunk_document(content, chunk_size, overlap)
        
        # Generate embeddings for chunks
        texts_with_metadata = []
        embeddings = []
        ids = []
        metadatas = []
        
        doc_id = str(uuid.uuid4())
        
        for i, chunk in enumerate(chunks):
            if not chunk.strip():
                continue
            
            chunk_id = f"{doc_id}_{i}"
            texts_with_metadata.append(chunk)
            embeddings.append(self.embedding_service.embed_text(chunk))
            ids.append(chunk_id)
            metadatas.append({
                "document_id": doc_id,
                "filename": filename,
                "chunk_index": i,
                "total_chunks": len(chunks)
            })
        
        # Add to ChromaDB
        if ids:
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=texts_with_metadata,
                metadatas=metadatas
            )
        
        return {
            "document_id": doc_id,
            "filename": filename,
            "chunks_added": len(ids)
        }
    
    def query(self, query: str, top_k: int = 5) -> List[dict]:
        """Query the document store for relevant chunks."""
        query_embedding = self.embedding_service.embed_text(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        
        formatted_results = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                formatted_results.append({
                    "content": doc,
                    "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                    "distance": results['distances'][0][i] if results['distances'] else 0
                })
        
        return formatted_results
    
    def get_document_count(self) -> int:
        """Get total number of documents (unique document IDs)."""
        count = self.collection.count()
        # This returns chunk count, approximate unique docs
        return count
    
    def delete_document(self, document_id: str) -> bool:
        """Delete a document by its ID."""
        # Get all chunks for this document
        results = self.collection.get(
            where={"document_id": document_id},
            include=[]
        )
        
        if results['ids']:
            self.collection.delete(ids=results['ids'])
            return True
        return False
    
    def list_documents(self) -> List[dict]:
        """List all unique documents."""
        results = self.collection.get(include=["metadatas"])
        
        seen_docs = {}
        for i, metadata in enumerate(results['metadatas']):
            doc_id = metadata.get('document_id')
            if doc_id and doc_id not in seen_docs:
                seen_docs[doc_id] = {
                    "document_id": doc_id,
                    "filename": metadata.get('filename', 'Unknown'),
                    "chunk_count": 0
                }
            if doc_id:
                seen_docs[doc_id]["chunk_count"] += 1
        
        return list(seen_docs.values())
