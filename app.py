# app.py
import streamlit as st
import os
import time
import pandas as pd
from PyPDF2 import PdfReader

from pipeline import process_file

def main():
    st.title("Metadata Extractor - Multi-file LLM-Enhanced")

    uploaded_files = st.file_uploader(
        "Upload up to 15 files (PDF, TXT, CSV, XLSX)",
        accept_multiple_files=True,
        type=["pdf", "txt", "csv", "xlsx"]
    )

    if uploaded_files:
        files_to_process = uploaded_files[:15]
        for uploaded_file in files_to_process:
            file_name = uploaded_file.name

            # Read once to get file size, then reset
            file_size = len(uploaded_file.read())
            uploaded_file.seek(0)

            with st.expander(f"Results for: {file_name}"):
                st.write(f"**File Name**: {file_name}")
                st.write(f"**File Size**: {file_size} bytes")

                # Save temp file so pipeline can process by path
                with open(file_name, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                temp_path = os.path.abspath(file_name)

                start_time = time.time()
                results = process_file(temp_path)
                end_time = time.time()

                file_type = results.get("file_type", "unknown")
                st.write(f"**Detected File Type**: {file_type}")

                # Check for top-level error
                if "error" in results:
                    st.error(results["error"])
                    # Clean up
                    os.remove(temp_path)
                    continue

                # -------------------------
                # Display Structure Metadata
                # -------------------------
                structure = results.get("structure", {})

                if file_type == "pdf":
                    pages = structure.get("pages", 0)
                    st.write(f"**Number of Pages**: {pages}")
                    length_of_text = structure.get("length_of_text", 0)
                    st.write(f"**Length of Extracted Text**: {length_of_text} chars")

                elif file_type == "text":
                    length_val = structure.get("length", 0)
                    lines_val = structure.get("lines", 0)
                    st.write(f"**Length**: {length_val} chars, **Lines**: {lines_val}")

                elif file_type in ["excel", "csv"]:
                    rows = structure.get("rows", 0)
                    cols = structure.get("cols", 0)
                    st.write(f"**Rows**: {rows}, **Columns**: {cols}")

                    # Factual data info
                    factual_data = structure.get("factual_data", {})
                    if factual_data:
                        st.write(f"**Factual Rows**: {factual_data.get('factual_rows', 0)}")
                        st.write(f"**Factual Columns**: {factual_data.get('factual_cols', 0)}")

                    # Suggested schema if available
                    raw_schema = structure.get("suggested_schema_raw")
                    if raw_schema:
                        st.write("**Suggested Schema (Raw)**:", raw_schema)

                # -------------------------
                # Display Abstracted Data
                # -------------------------
                abstracted = results.get("abstracted_data", {})

                # 1. Chapter Summaries
                #    If pipeline found multiple chapters, it might store them here.
                if "chapter_summaries" in abstracted:
                    st.subheader("Chapter Summaries")
                    for chapter_sum in abstracted["chapter_summaries"]:
                        st.write(chapter_sum)

                # 2. Full Doc Summary
                elif "full_doc_summary" in abstracted:
                    st.subheader("Entire Document Summary")
                    st.write(abstracted["full_doc_summary"])

                # 3. Data Insights for Excel/CSV
                if file_type in ["excel", "csv"] and "insights" in abstracted:
                    st.subheader("Data Insights from LLM")
                    st.write(abstracted["insights"])

                # Additional errors or info
                if "error" in abstracted:
                    st.error(abstracted["error"])

                st.write(f"**Processing Time**: {end_time - start_time:.2f} seconds")

                # Cleanup - remove local temp file
                os.remove(temp_path)

if __name__ == "__main__":
    main()
