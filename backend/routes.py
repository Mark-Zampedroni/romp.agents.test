from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from .store import DocumentStore
from .schemas import QueryRequest, QueryResponse, HealthResponse
import os
import tempfile
from .parser import DocumentParser

router = APIRouter()
document_store = DocumentStore()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "document_count": document_store.get_document_count()
    }

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a document for indexing."""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        try:
            # Parse document
            text_content = DocumentParser.parse(tmp_path)
            
            # Add to document store
            result = document_store.add_document(file.filename, text_content)
            
            return {
                "success": True,
                "message": "Document uploaded successfully",
                "data": result
            }
        finally:
            # Clean up temp file
            os.unlink(tmp_path)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")

@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query documents using RAG."""
    try:
        # Get relevant chunks
        results = document_store.query(request.query, request.top_k)
        
        if not results:
            return QueryResponse(
                query=request.query,
                results=[],
                answer="No relevant documents found. Please upload some documents first."
            )
        
        # Build context from results
        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(f"[Source: {result['metadata'].get('filename', 'Unknown')}]\n{result['content']}")
        
        context = "\n\n".join(context_parts)
        
        # Generate answer using the context
        # Simple approach: extract relevant sentences from context
        query_lower = request.query.lower()
        answer_parts = []
        
        for result in results:
            content = result['content']
            # Find sentences that might answer the query
            sentences = content.replace('?', '.').replace('!', '.').split('.')
            for sentence in sentences:
                sentence = sentence.strip()
                if sentence and any(word in sentence.lower() for word in query_lower.split() if len(word) > 3):
                    answer_parts.append(sentence)
        
        if answer_parts:
            answer = " ".join(answer_parts[:5])  # Limit answer length
        else:
            # Fallback: use first chunk
            answer = results[0]['content'][:500]
        
        return QueryResponse(
            query=request.query,
            results=results,
            answer=answer
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

@router.get("/documents")
async def list_documents():
    """List all uploaded documents."""
    documents = document_store.list_documents()
    return {"documents": documents}

@router.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete a document."""
    success = document_store.delete_document(document_id)
    if success:
        return {"success": True, "message": "Document deleted"}
    raise HTTPException(status_code=404, detail="Document not found")
