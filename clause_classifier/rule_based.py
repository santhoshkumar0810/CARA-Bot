from typing import List, Dict

CLAUSE_KEYWORDS = {
    "Termination": ["terminate", "termination", "cancel", "cancellation", "end of agreement", "material breach"],
    "Indemnity": ["indemnify", "indemnification", "hold harmless", "defend against claims", "liability for"],
    "Confidentiality": ["confidential information", "proprietary data", "trade secret", "non-disclosure"],
    "Payment": ["payment terms", "invoicing", "fees", "compensation", "taxes", "currency"],
    "Liability": ["limitation of liability", "indirect damages", "consequential damages", "total liability", "cap on liability"],
    "Jurisdiction": ["governing law", "jurisdiction", "venue", "courts of", "dispute resolution", "arbitration"],
    "Non-Compete": ["non-compete", "non-solicitation", "exclusivity", "restrictive covenants"],
    "Intellectual Property": ["intellectual property", "ownership of work", "copyright", "patent", "assignment of rights"]
}

def classify_clause_rule_based(text: str) -> Dict[str, float]:
    """
    Classifies a clause based on keyword presence.
    Returns a dictionary of Label -> Confidence Score.
    """
    text_lower = text.lower()
    scores = {}
    
    for label, keywords in CLAUSE_KEYWORDS.items():
        matches = sum(1 for kw in keywords if kw in text_lower)
        if matches > 0:
            # Simple scoring: 0.5 for 1 match, 0.8 for 2+, capped at 1.0
            score = 0.5 if matches == 1 else 0.8
            scores[label] = score
            
    return scores
