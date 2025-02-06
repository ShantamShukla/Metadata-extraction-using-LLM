import logging
import json
import os
import pandas as pd

from file_detection import detect_file_type
from data_extraction import (
    extract_text_data, extract_excel_data, extract_csv_data, extract_pdf_data
)
from preprocessing import preprocess_text
from llm_utils import (
    infer_schema_with_llm,
    summarize_text_with_llm,
    generate_data_insights_with_llm,
    summarize_chapters  # <--- The new function to handle chapters
)

logger = logging.getLogger(__name__)

def identify_factual_data(df: pd.DataFrame):
    """
    Determines how many rows and columns in the DataFrame
    contain actual (non-empty) data.
    """
    non_empty_cols = sum(df.notna().any(axis=0))
    non_empty_rows = sum(df.notna().any(axis=1))
    return non_empty_rows, non_empty_cols

def process_file(file_path: str) -> dict:
    """
    1. Detect file type
    2. Extract data
    3. Summarize or infer schema
    4. Return structured results: metadata + LLM insights
    """
    if not os.path.isfile(file_path):
        return {
            "file_path": file_path,
            "file_type": "unknown",
            "error": "File does not exist."
        }

    file_type = detect_file_type(file_path)
    results = {
        "file_path": file_path,
        "file_type": file_type,
        "structure": {},
        "abstracted_data": {}
    }

    # -------------------------
    # Handle PDF
    # -------------------------
    if file_type == "pdf":
        pdf_text = extract_pdf_data(file_path)
        # Count pages
        try:
            import PyPDF2
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                page_count = len(reader.pages)
        except:
            page_count = 0

        cleaned_text = preprocess_text(pdf_text)

        # 1) Summarize chapters if present
        chapter_summaries = summarize_chapters(pdf_text, model="gpt-4o-mini")
        if chapter_summaries:
            # We found multiple chapters, so store them
            results["abstracted_data"]["chapter_summaries"] = chapter_summaries
        else:
            # 2) Fallback to single doc summary
            doc_summary = summarize_text_with_llm(cleaned_text, model="gpt-4o-mini")
            results["abstracted_data"]["full_doc_summary"] = doc_summary

        results["structure"]["pages"] = page_count
        results["structure"]["length_of_text"] = len(cleaned_text)
        # Optionally store the raw text
        results["raw_text"] = pdf_text

    # -------------------------
    # Handle Plain Text
    # -------------------------
    elif file_type == "text":
        raw_text = extract_text_data(file_path)
        cleaned_text = preprocess_text(raw_text)

        chapter_summaries = summarize_chapters(raw_text, model="gpt-4o-mini")
        if chapter_summaries:
            # Found multiple chapters
            results["abstracted_data"]["chapter_summaries"] = chapter_summaries
        else:
            # Single summary
            doc_summary = summarize_text_with_llm(cleaned_text, model="gpt-4o-mini")
            results["abstracted_data"]["full_doc_summary"] = doc_summary

        results["structure"]["length"] = len(cleaned_text)
        results["structure"]["lines"] = raw_text.count("\n") + 1
        results["raw_text"] = raw_text

    # -------------------------
    # Handle Excel
    # -------------------------
    elif file_type == "excel":
        df = extract_excel_data(file_path)
        if df.empty:
            results["abstracted_data"]["error"] = "Excel file extraction failed or empty."
            return results

        rows, cols = df.shape
        results["structure"]["rows"] = rows
        results["structure"]["cols"] = cols

        # Factual data check
        factual_rows, factual_cols = identify_factual_data(df)
        results["structure"]["factual_data"] = {
            "factual_rows": factual_rows,
            "factual_cols": factual_cols
        }

        # LLM-based schema suggestion
        sample_rows = df.head(5).values.tolist()
        schema_suggestion = infer_schema_with_llm(sample_rows)
        results["structure"]["suggested_schema_raw"] = schema_suggestion

        # Try parsing column suggestions as JSON
        try:
            column_names = json.loads(schema_suggestion)
            if len(column_names) == df.shape[1]:
                df.columns = column_names
        except Exception as e:
            logger.warning(f"Failed to parse schema suggestion: {e}")

        # Data insights from LLM
        data_insights = generate_data_insights_with_llm(df)
        results["abstracted_data"]["insights"] = data_insights

    # -------------------------
    # Handle CSV
    # -------------------------
    elif file_type == "csv":
        df = extract_csv_data(file_path)
        if df.empty:
            results["abstracted_data"]["error"] = "CSV file extraction failed or empty."
            return results

        rows, cols = df.shape
        results["structure"]["rows"] = rows
        results["structure"]["cols"] = cols

        # Factual data check
        factual_rows, factual_cols = identify_factual_data(df)
        results["structure"]["factual_data"] = {
            "factual_rows": factual_rows,
            "factual_cols": factual_cols
        }

        # LLM-based schema suggestion
        sample_rows = df.head(5).values.tolist()
        schema_suggestion = infer_schema_with_llm(sample_rows)
        results["structure"]["suggested_schema_raw"] = schema_suggestion

        try:
            column_names = json.loads(schema_suggestion)
            if len(column_names) == df.shape[1]:
                df.columns = column_names
        except Exception as e:
            logger.warning(f"Failed to parse schema suggestion: {e}")

        data_insights = generate_data_insights_with_llm(df)
        results["abstracted_data"]["insights"] = data_insights

    # -------------------------
    # Unsupported File
    # -------------------------
    else:
        results["abstracted_data"]["error"] = "Unsupported file type or detection failed."

    return results
