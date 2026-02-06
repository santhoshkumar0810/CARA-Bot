import spacy
from typing import List, Dict

# Load the model globally to avoid reloading (lazy loading pattern in app is better, but this is simple)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Fallback or placeholder, handled by main setup usually
    nlp = None

def extract_entities(text: str) -> Dict[str, List[str]]:
    """
    Extracts standard legal entities using spaCy.
    Groups by type: Parties (ORG/PERSON), Dates, Money, Locations.
    """
    if not nlp:
        return {"Error": ["Model en_core_web_sm not loaded"]}

    doc = nlp(text)
    
    entities = {
        "PARTIES": [],
        "DATES": [],
        "MONEY": [],
        "JURISDICTION": []
    }
    
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PERSON"]:
            if ent.text not in entities["PARTIES"]: # precise dedupe needed later
                entities["PARTIES"].append(ent.text)
        elif ent.label_ == "DATE":
            entities["DATES"].append(ent.text)
        elif ent.label_ == "MONEY":
            entities["MONEY"].append(ent.text)
        elif ent.label_ == "GPE": # Geopolitical Entity often implies Jurisdiction
            entities["JURISDICTION"].append(ent.text)
            
    # Simple list deduplication
    for k in entities:
        entities[k] = list(set(entities[k]))
        
    return entities
