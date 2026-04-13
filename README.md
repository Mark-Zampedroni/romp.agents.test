# RAG Document Q&A System

A Retrieval-Augmented Generation (RAG) system that lets you upload documents and ask questions about their content using embeddings.

## Features

- ð **Multi-format Support**: Upload PDF, DOCX, TXT, and MD files
- ð **Semantic Search**: Uses sentence transformers for intelligent embeddings
- ð¬ **Natural Language Q&A**: Ask questions in plain English
- ð¨ **Modern UI**: Clean, responsive web interface
- ð **Source Attribution**: See which documents your answers come from

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python main.py
```

### 3. Open the Web Interface

Navigate to `http://localhost:8000` in your browser.

## API Endpoints

- `GET /` - Web interface
- `POST /api/upload` - Upload a document (multipart/form-data)
- `POST /api/query` - Ask a question about documents
- `GET /api/documents` - List all uploaded documents
- `DELETE /api/documents/{id}` - Delete a document
- `GET /health` - Health check

## How It Works

1. **Upload**: Documents are parsed and split into overlapping chunks
2. **Embed**: Each chunk is converted to a vector embedding using `all-MiniLM-L6-v2`
3. **Store**: Embeddings are stored in ChromaDB for fast similarity search
4. **Query**: Questions are embedded and matched against document chunks
5. **Answer**: Relevant chunks are extracted and presented as the answer

## Tech Stack

- **Backend**: FastAPI, ChromaDB, Sentence Transformers
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Embeddings**: all-MiniLM-L6-v2 (384 dimensions)
- **Document Parsing**: PyPDF2, python-docx

## Example Usage

### Upload a document via curl:
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@/path/to/your/document.pdf"
```

### Ask a question:
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the main topic?", "top_k": 5}'
```

## Configuration

Environment variables:
- `CHROMA_PERSIST_DIR` - Directory for ChromaDB persistence (default: `./chroma_db`)

## License

MIT
