def translate_to_english(text: str, source_lang: str) -> str:
    """
    Translates text to English.
    Currently a mock stub. Use a real API (Google/DeepL/LLM) here.
    """
    if source_lang == 'en':
        return text
        
    return f"[TRANSLATED from {source_lang}]: {text}"
