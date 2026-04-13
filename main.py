from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.routes import router
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="RAG Document Q&A API",
    description="Upload documents and ask questions using RAG with embeddings",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount frontend static files
frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
async def root():
    return FileResponse(os.path.join(frontend_dir, 'index.html'))

# Include API routes
app.include_router(router, prefix="/api")

@app.get("/health")
async def health():
    from backend.store import DocumentStore
    store = DocumentStore()
    return {"status": "healthy", "documents": store.get_document_count()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
