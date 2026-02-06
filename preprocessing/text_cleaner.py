import re

def clean_text(text: str) -> str:
    """
    Normalizes the input text:
    - Removes excessive whitespace/newlines.
    - Standardizes quotes/dashes.
    - Tries to remove common header/footer garbage (page numbers mostly).
    """
    # Normalize unicode characters (e.g. smart quotes)
    text = text.replace('“', '"').replace('”', '"').replace("‘", "'").replace("’", "'")
    
    # Remove page numbers like "Page 1 of 10" or just isolated numbers at start/end of lines
    # (Simple heuristic)
    text = re.sub(r'\n\s*Page \d+ of \d+\s*\n', '\n', text, flags=re.IGNORECASE)
    
    # Compress multiple newlines to max 2 (preserve paragraph structure)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    # Compress multiple spaces
    text = re.sub(r'[ \t]+', ' ', text)
    
    return text.strip()
