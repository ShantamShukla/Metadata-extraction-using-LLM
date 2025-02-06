# preprocessing.py
import logging

logger = logging.getLogger(__name__)

def preprocess_text(raw_text: str) -> str:
    """
    Removes extra newlines, spaces, etc., preparing text for LLM.
    """
    if not raw_text:
        return ""

    cleaned = raw_text.replace("\r", " ").replace("\n", " ").strip()
    logger.debug(f"Preprocessed text length: {len(cleaned)}")
    return cleaned
