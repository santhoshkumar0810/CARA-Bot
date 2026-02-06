from typing import Dict
import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_clause_explanation(clause_text: str, risk_info: Dict) -> Dict[str, str]:
    """
    Generates an explanation for a contract clause using Groq LLM.
    """

    api_key = os.getenv("GROQ_API")

    if not api_key:
        return {
            "plain_explanation": "API key missing.",
            "why_risky": "GROQ_API_KEY not found in environment.",
            "business_impact": "Unknown",
            "suggested_alternative": "Check system configuration."
        }

    client = Groq(api_key=api_key)

    risk_reason = risk_info.get("reason", "No specific risk detected")
    risk_severity = risk_info.get("severity", "Neutral")

    prompt = f"""
You are a legal assistant for Indian small businesses.

Analyze the following contract clause and RETURN ONLY VALID JSON.
Do not include explanations or markdown.

Clause:
\"\"\"{clause_text}\"\"\"

Detected Risk Level: {risk_severity}
Detected Risk Reason: {risk_reason}

Return JSON with EXACTLY these keys:
- plain_explanation
- why_risky
- business_impact
- suggested_alternative
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a legal AI assistant. Output JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=512
        )

        content = response.choices[0].message.content.strip()

        # Safety: ensure valid JSON
        return json.loads(content)

    except json.JSONDecodeError:
        return {
            "plain_explanation": "Model output was not valid JSON.",
            "why_risky": "LLM formatting error.",
            "business_impact": "Unknown",
            "suggested_alternative": "Retry with stricter prompt."
        }

    except Exception as e:
        return {
            "plain_explanation": "Error calling Groq API.",
            "why_risky": str(e),
            "business_impact": "None",
            "suggested_alternative": "Retry later."
        }

