import re
from typing import List, Dict

def extract_clauses_from_text(text: str) -> List[Dict[str, str]]:
    """
    Splits the contract text into clauses.
    Strategy:
    1. Try to detect numbered clauses (e.g. "1. Term", "1.1. Commencement").
    2. If found, split based on these.
    3. If not found, fall back to splitting by double newlines (paragraphs).
    
    Returns a list of dicts: {"clause_id": str, "text": str, "title": str}
    """
    clauses = []
    
    # Regex for standard numbering: Start of line, number, dot, space.
    # Captures: (Number) (Optional Title)
    # Examples: "1. Term", "2.1 Termination", "ARTICLE 1: DEFINITIONS"
    
    # Simple pattern: Number followed by dot
    clause_pattern = re.compile(r'(?:^|\n)(\d+(?:\.\d+)*)\.?\s*(.*?)(?=\n\d+(?:\.\d+)*\.?|\Z)', re.DOTALL)
    
    matches = list(clause_pattern.finditer(text))
    
    if len(matches) > 3: # Arbitrary threshold to decide if structure exists
        for match in matches:
            clause_id = match.group(1)
            content = match.group(2).strip()
            
            # extract title if it looks like the first line is caps or short
            lines = content.split('\n')
            first_line = lines[0].strip()
            title = ""
            
            if len(first_line) < 50 and (first_line.isupper() or first_line.istitle()):
                title = first_line
                # Remove title from content if desired, or keep it. Keeping it is safer for context.
            
            clauses.append({
                "clause_id": clause_id,
                "text": content,
                "title": title
            })
    else:
        # Fallback: Paragraph splitting
        paragraphs = text.split('\n\n')
        for i, para in enumerate(paragraphs):
            if para.strip():
                # Try to guess a minimal title or just use ID
                clauses.append({
                    "clause_id": str(i + 1),
                    "text": para.strip(),
                    "title": ""
                })
                
    return clauses
