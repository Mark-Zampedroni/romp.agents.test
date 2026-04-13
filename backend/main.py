from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
import os

def create_app():
    """Create and configure the FastAPI application."""
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
    
    # Include routes
    app.include_router(router, prefix="/api")
    
    @app.get("/")
    async def root():
        return {
            "message": "RAG Document Q&A API",
            "docs": "/docs",
            "health": "/api/health"
        }
    
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
