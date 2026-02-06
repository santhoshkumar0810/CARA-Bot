import pdfplumber
import os

def read_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF file using pdfplumber.
    Raises ValueError if the PDF appears to be scanned (no text extracted).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    text_content = []
    
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_content.append(text)
    
    full_text = "\n".join(text_content)
    
    if not full_text.strip():
        raise ValueError("No text extracted. The PDF might be scanned or empty.")
        
    return full_text
