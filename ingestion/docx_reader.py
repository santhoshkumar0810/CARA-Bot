from docx import Document
import os

def read_docx(file_path: str) -> str:
    """
    Extracts text from a DOCX file using python-docx.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            if para.text.strip():
                full_text.append(para.text)
        return "\n".join(full_text)
    except Exception as e:
        raise RuntimeError(f"Failed to read DOCX file: {e}")
