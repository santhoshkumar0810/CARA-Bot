import yaml
import os
from typing import List, Dict

def load_risk_rules(rules_path: str) -> Dict:
    """Loads the YAML risk rules."""
    if not os.path.exists(rules_path):
        return {}
    with open(rules_path, 'r') as f:
        return yaml.safe_load(f)

def evaluate_risk(clause_text: str, category: str, rules_db: Dict) -> List[Dict]:
    """
    Evaluates a clause text against rules for a specific category.
    Returns details of any risks found.
    """
    risks = []
    category_rules = rules_db.get(category, [])
    
    text_lower = clause_text.lower()
    
    for rule in category_rules:
        risk_found = False
        
        # Keyword check
        if 'keyword' in rule and rule['keyword'] in text_lower:
            risk_found = True
            
        # Negative keyword check (Risk if keyword IS PRESENT but negative_keyword IS NOT)
        # Example: "laws of" (Risk) but "India" (Safe) -> Risk if "laws of" in text AND "India" NOT in text.
        if 'negative_keyword' in rule:
            if rule['keyword'] in text_lower and rule['negative_keyword'] not in text_lower:
                risk_found = True
            else:
                risk_found = False # Reset if safety word is present
                
        # Condition check (Mock logic for specific complex conditions)
        if 'condition' in rule:
            if rule['condition'] == 'no_cap' and ('cap' not in text_lower and 'limit' not in text_lower):
                 # Weak heuristic: if Indemnity clause doesn't mention 'cap' or 'limit', flag it.
                 risk_found = True
            elif rule['condition'] == 'unilateral' and ('without cause' in text_lower or 'at its sole discretion' in text_lower):
                 risk_found = True

        if risk_found:
            risks.append({
                "risk_id": rule['id'],
                "severity": rule['severity'],
                "reason": rule['reason'],
                "clause_text": clause_text[:100] + "..." # Snippet
            })
            
    return risks
