import logging
import json
import pandas as pd

from file_detection import detect_file_type
from data_extraction import (
    extract_text_data, extract_excel_data, extract_csv_data, extract_pdf_data
)
from preprocessing import preprocess_text
from llm_utils import (
    infer_schema_with_llm, summarize_text_with_llm, generate_data_insights_with_llm, call_llm
)

logger = logging.getLogger(__name__)

def process_file(file_path: str) -> dict:
    """
    Orchestrates the entire process for a single file.

    Args:
        file_path (str): Path to the file.

    Returns:
        dict: Results containing structure info and abstracted data from the LLM.
    """
    file_type = detect_file_type(file_path)
    results = {
        "file_path": file_path,
        "file_type": file_type,
        "structure": None,       # e.g. metadata, schema
        "abstracted_data": None  # e.g. summary, insights
    }

    if file_type == "text":
        raw_text = extract_text_data(file_path)
        cleaned_text = preprocess_text(raw_text)
        summary = summarize_text_with_llm(cleaned_text)

        results["structure"] = {
            "length": len(cleaned_text),
            "lines": raw_text.count("\n") + 1
        }
        results["abstracted_data"] = {
            "summary": summary
        }

    elif file_type == "excel":
        df = extract_excel_data(file_path)
        if not df.empty:
            # Infer schema from first few rows
            sample_rows = df.head(5).values.tolist()
            schema_suggestion = infer_schema_with_llm(sample_rows)

            # Attempt to parse LLM JSON
            try:
                column_names = json.loads(schema_suggestion)
                if len(column_names) == df.shape[1]:
                    df.columns = column_names
            except Exception as e:
                logger.warning(f"Failed to parse schema suggestion: {e}")

            data_insights = generate_data_insights_with_llm(df)

            results["structure"] = {
                "rows": df.shape[0],
                "cols": df.shape[1],
                "sample_data": df.head(3).to_dict(orient="records"),
                "suggested_schema": schema_suggestion
            }
            results["abstracted_data"] = {
                "insights": data_insights
            }
        else:
            results["abstracted_data"] = {"error": "Excel file extraction failed or empty."}
    
    elif file_type == "pdf":
        raw_text = extract_pdf_data(file_path)
        cleaned_text = preprocess_text(raw_text)
        summary = summarize_text_with_llm(cleaned_text)
        results["structure"] = {
            "length": len(cleaned_text),
            "lines": raw_text.count("\n") + 1
        }
        results["abstracted_data"] = {
            "summary": summary
        }

    elif file_type == "csv":
        df = extract_csv_data(file_path)
        if not df.empty:
            sample_rows = df.head(5).values.tolist()
            schema_suggestion = infer_schema_with_llm(sample_rows)

            # Attempt to parse LLM JSON
            try:
                column_names = json.loads(schema_suggestion)
                if len(column_names) == df.shape[1]:
                    df.columns = column_names
            except Exception as e:
                logger.warning(f"Failed to parse schema suggestion: {e}")

            data_insights = generate_data_insights_with_llm(df)

            results["structure"] = {
                "rows": df.shape[0],
                "cols": df.shape[1],
                "sample_data": df.head(3).to_dict(orient="records"),
                "suggested_schema": schema_suggestion
            }
            results["abstracted_data"] = {
                "insights": data_insights
            }
        else:
            results["abstracted_data"] = {"error": "CSV file extraction failed or empty."}

    else:
        results["abstracted_data"] = {"error": "Unsupported file type or detection failed."}

    return results