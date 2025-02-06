# file_detection.py
import logging
import os

try:
    import magic
except ImportError:
    magic = None

logger = logging.getLogger(__name__)

def detect_file_type(file_path: str) -> str:
    """
    Detect file type using python-magic if available.
    Fallback to extension-based detection if magic is not installed or fails.
    """
    if not os.path.isfile(file_path):
        logger.error(f"File does not exist: {file_path}")
        return "unknown"

    if magic is not None:
        try:
            mime = magic.from_file(file_path, mime=True)
            logger.info(f"MIME type detected for {file_path}: {mime}")
            if "pdf" in mime:
                return "pdf"
            elif "text" in mime:
                return "text"
            elif "excel" in mime or "spreadsheet" in mime:
                return "excel"
            elif "csv" in mime:
                return "csv"
            else:
                return "unknown"
        except Exception as e:
            logger.warning(f"Error using python-magic: {e}")

    # Fallback to extension-based detection
    ext = os.path.splitext(file_path)[-1].lower()
    logger.info(f"Falling back to extension detection for {file_path} with ext {ext}")
    if ext in [".txt", ".md", ".log"]:
        return "text"
    elif ext in [".xlsx", ".xls"]:
        return "excel"
    elif ext == ".csv":
        return "csv"
    elif ext == ".pdf":
        return "pdf"
    else:
        return "unknown"
