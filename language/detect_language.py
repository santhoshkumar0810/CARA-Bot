from langdetect import detect, LangDetectException

def detect_language_code(text: str) -> str:
    """
    Detects the language of the text.
    Returns ISO 639-1 code (e.g., 'en', 'hi').
    Returns 'unknown' on failure.
    """
    try:
        # Use a sample of text to speed up detection
        sample = text[:1000] if len(text) > 1000 else text
        return detect(sample)
    except LangDetectException:
        return 'unknown'
