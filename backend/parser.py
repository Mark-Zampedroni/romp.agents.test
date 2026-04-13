from PyPDF2 import PdfReader
from docx import Document
from typing import Optional

class DocumentParser:
    """Parse various document formats."""
    
    @staticmethod
    def parse_pdf(file_path: str) -> str:
        """Extract text from PDF file."""
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n\n"
        return text.strip()
    
    @staticmethod
    def parse_docx(file_path: str) -> str:
        """Extract text from DOCX file."""
        doc = Document(file_path)
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        return "\n\n".join(paragraphs)
    
    @staticmethod
    def parse_txt(file_path: str) -> str:
        """Read plain text file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    
    @classmethod
    def parse(cls, file_path: str, file_type: Optional[str] = None) -> str:
        """Parse file based on extension or provided type."""
        if not file_type:
            file_type = file_path.split('.')[-1].lower()
        
        parsers = {
            'pdf': cls.parse_pdf,
            'docx': cls.parse_docx,
            'txt': cls.parse_txt,
            'md': cls.parse_txt,
        }
        
        parser = parsers.get(file_type)
        if not parser:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        return parser(file_path)
