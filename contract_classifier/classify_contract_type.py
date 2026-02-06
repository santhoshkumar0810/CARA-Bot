import re
from typing import Dict

CONTRACT_KEYWORDS = {
    "Non-Disclosure Agreement": ["non-disclosure", "confidentiality", "nda", "proprietary information"],
    "Service Agreement": ["service agreement", "scope of services", "deliverables", "master service agreement", "msa"],
    "Employment Agreement": ["employment agreement", "offer of employment", "employee", "salary", "probation"],
    "Lease Agreement": ["lease agreement", "lessor", "lessee", "rent", "premises"],
    "Software License": ["software license", "eula", "licensor", "licensee", "source code"]
}

def classify_contract_type(text: str) -> Dict[str, any]:
    """
    Classifies the contract type based on keyword frequency in the first 2000 characters.
    Returns: {"contract_type": str, "confidence": float}
    """
    # Focus on the beginning of the document
    header_text = text[:2000].lower()
    
    scores = {ctype: 0 for ctype in CONTRACT_KEYWORDS}
    
    for ctype, keywords in CONTRACT_KEYWORDS.items():
        for kw in keywords:
            if kw in header_text:
                scores[ctype] += 1
                
    # Find max score
    if not scores:
        return {"contract_type": "Unknown", "confidence": 0.0}
        
    best_match = max(scores, key=scores.get)
    score = scores[best_match]
    
    # Simple confidence normalization
    if score >= 2:
        confidence = 0.9
    elif score == 1:
        confidence = 0.6
    else:
        confidence = 0.0
        best_match = "Unknown"
        
    return {"contract_type": best_match, "confidence": confidence}
