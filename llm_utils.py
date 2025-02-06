import logging
import json
import openai
import pandas as pd
from typing import List
import re
from config import OPENAI_API_KEY

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------
# OpenAI API Config
# ---------------------------------------------------------------------
openai.api_key = OPENAI_API_KEY

def call_llm(prompt: str, model: str = "gpt-4o-mini", max_tokens: int = 600) -> str:
    """
    Generic helper to call the OpenAI ChatCompletion API.
    """
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY not set. Cannot call LLM.")
        return ""

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )
        output = response.choices[0].message.content.strip()
        logger.debug(f"LLM response: {output}")
        return output
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        return ""

def infer_schema_with_llm(sample_rows, model: str = "gpt-4o-mini") -> str:
    """
    Prompt the LLM to suggest headers/column names for a table without headers.
    Returns a JSON-encoded list of suggested column headers (if successful).
    """
    prompt = f"""
The following data rows do not have headers:
{sample_rows}

Suggest likely column headers (one per column), and return ONLY a JSON list of strings.
For example: ["ID", "Name", "Date", "Amount"].
"""
    schema_suggestion = call_llm(prompt, model=model, max_tokens=3000)
    return schema_suggestion

def summarize_text_with_llm(cleaned_text: str, model: str = "gpt-4o-mini") -> str:
    """
    Summarize large text using an LLM (single-call approach).
    If text is extremely large, you may still risk token-limit errors.
    """
    if len(cleaned_text) < 10:
        return "No meaningful text to summarize."

    prompt = f"""
Summarize the following text in a concise, high-level manner:
{cleaned_text}
"""
    summary = call_llm(prompt, model=model, max_tokens=3000)
    return summary

def generate_data_insights_with_llm(df, model: str = "gpt-4o-mini") -> str:
    """
    Provide a high-level analysis of a DataFrame using an LLM.
    """
    if df.empty:
        return "No data available for analysis."

    sample_str = df.head(5).to_csv(index=False)
    prompt = f"""
Below is a sample of tabular data (up to 5 rows). Provide a high-level analysis:
{sample_str}

Potential areas to address:
- Data categories
- Trends or anomalies
- Potential relationships
"""
    analysis = call_llm(prompt, model=model, max_tokens=3000)
    return analysis

# ---------------------------------------------------------------------
# Chunking + Large-Text Summaries (to avoid token limit issues)
# ---------------------------------------------------------------------
# def chunk_text(text: str, chunk_size: int = 3000) -> List[str]:
#     """
#     Splits 'text' into chunks of approximately 'chunk_size' characters
#     to avoid exceeding token limits in a single LLM call.
#     """
#     words = text.split()
#     chunks = []
#     current_chunk = []
#     current_length = 0

#     for word in words:
#         current_chunk.append(word)
#         current_length += len(word) + 1  # +1 for space
#         if current_length >= chunk_size:
#             chunks.append(" ".join(current_chunk))
#             current_chunk = []
#             current_length = 0

#     if current_chunk:
#         chunks.append(" ".join(current_chunk))

#     return chunks

# def summarize_large_text(full_text: str, model: str = "gpt-4o-mini") -> str:
#     """
#     Breaks the 'full_text' into smaller chunks, summarizes each chunk with
#     'summarize_text_with_llm()', then combines partial summaries for a final result.
#     """
#     chunks = chunk_text(full_text, chunk_size=3000)
#     if not chunks:
#         return "No meaningful text to summarize."

#     partial_summaries = []
#     for i, chunk_data in enumerate(chunks):
#         partial_summary = summarize_text_with_llm(chunk_data, model=model)
#         partial_summaries.append(f"Chunk {i+1} Summary:\n{partial_summary}")

#     combined_prompt = (
#         "Combine the following partial summaries into a single, concise overview:\n\n"
#         + "\n\n".join(partial_summaries)
#     )
#     final_summary = call_llm(combined_prompt, model=model, max_tokens=1000)
#     return final_summary

def detect_chapters(text: str) -> list:
    """
    Splits 'text' by lines containing 'Chapter <digits>' or 'CHAPTER <digits>'.
    If multiple chapters are found, returns them as separate sections.
    Otherwise returns a single-element list (the entire text).
    """
    # A naive regex looking for lines that start with 'Chapter <digits>'
    chapters = re.split(r'(?i)(?:^|\n)chapter\s+\d+', text)
    # If we only got 1 chunk, it means no real chapters were found
    return chapters if len(chapters) > 1 else [text]

def summarize_chapters(text: str, model: str = "gpt-4o-mini") -> list:
    """
    Detects 'Chapter' headings and summarizes each as a separate piece.
    If there's only one piece (no chapters), we'll rely on pipeline fallback.
    """
    sections = detect_chapters(text)
    summaries = []

    # If there's only 1 'section', it's effectively the entire doc
    if len(sections) == 1:
        return summaries  # We do no chunking or multi-summaries here

    # Summarize each chapter
    for i, chapter_text in enumerate(sections, start=1):
        # skip trivial lines
        if len(chapter_text.strip()) < 50:
            continue
        summary = summarize_text_with_llm(chapter_text, model=model)
        summaries.append(f"Chapter {i} Summary:\n{summary}")

    return summaries
