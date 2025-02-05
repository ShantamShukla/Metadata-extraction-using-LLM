import logging
import pandas as pd
import PyPDF2 

logger = logging.getLogger(__name__)

def extract_text_data(file_path: str) -> str:
    """
    Extract raw text from a text file.

    Args:
        file_path (str): Path to the text file.

    Returns:
        str: The entire text content.
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            data = f.read()
        logger.info(f"Extracted text from {file_path} (length={len(data)})")
        return data
    except Exception as e:
        logger.error(f"Error reading text file {file_path}: {e}")
        return ""

def extract_excel_data(file_path: str):
    """
    Extract data from an Excel file using pandas.
    Reads the first sheet with no header.

    Args:
        file_path (str): Path to the Excel file.

    Returns:
        pd.DataFrame: Pandas DataFrame with the file's contents.
    """
    try:
        df = pd.read_excel(file_path, sheet_name=0, header=None)
        logger.info(f"Extracted Excel data from {file_path}, shape={df.shape}")
        return df
    except Exception as e:
        logger.error(f"Error reading Excel file {file_path}: {e}")
        return pd.DataFrame()

def extract_csv_data(file_path: str):
    """
    Extract data from a CSV file using pandas.
    Reads with no header.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Pandas DataFrame with the file's contents.
    """
    try:
        df = pd.read_csv(file_path, header=None)
        logger.info(f"Extracted CSV data from {file_path}, shape={df.shape}")
        return df
    except Exception as e:
        logger.error(f"Error reading CSV file {file_path}: {e}")
        return pd.DataFrame()

def extract_pdf_data(file_path: str) -> str:
    """
    Extract raw text from a PDF file using PyPDF2.
    Returns all text as a single string.
    """
    text_content = []
    try:
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            # For older versions of PyPDF2, pages might be read differently
            for page in pdf_reader.pages:
                extracted = page.extract_text() or ""
                text_content.append(extracted)
        final_text = "\n".join(text_content)
        logger.info(f"Extracted PDF data from {file_path}, length={len(final_text)}")
        return final_text
    except Exception as e:
        logger.error(f"Error reading PDF file {file_path}: {e}")
        return ""