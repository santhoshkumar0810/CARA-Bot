from typing import List

INTENT_MAPPING = {
    "Obligation": ["shall", "must", "will", "agrees to", "is required to"],
    "Right": ["may", "has the right", "entitled to", "can", "option to"],
    "Prohibition": ["shall not", "must not", "will not", "prohibited from", "restricted from"],
    "Definition": ["means", "refers to", "defined as"] # Extra helper
}

def detect_clause_intent(text: str) -> List[str]:
    """
    Detects legal intent (Obligation, Right, Prohibition) based on modal verbs.
    Returns a list of detected intents.
    """
    text_lower = text.lower()
    detected_intents = []
    
    for intent, keywords in INTENT_MAPPING.items():
        for kw in keywords:
            # Check for keyword with word boundaries to avoid partial matches naturally
            # For simplicity using ' in ' checks which is robust enough for "shall not" etc.
            if f" {kw} " in f" {text_lower} ":
                detected_intents.append(intent)
                break
                
    return detected_intents if detected_intents else ["Information"]
