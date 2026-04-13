#!/bin/bash
cd /app
pip install --break-system-packages fastapi uvicorn python-multipart sentence-transformers chromadb pypdf2 python-docx pydantic
python main.py
