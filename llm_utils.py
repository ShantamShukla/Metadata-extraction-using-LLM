import logging
import json
import openai
# import google.generativeai as palm  # Hypothetical import

# from config import GEMINI_API_KEY 
from config import OPENAI_API_KEY

logger = logging.getLogger(__name__)

def call_llm(prompt: str, model: str = "gpt-4o-mini", max_tokens: int = 600) -> str:
    """
    Call an OpenAI ChatCompletion API.

    Args:
        prompt (str): The text prompt for the LLM.
        model (str): Which model to use.
        max_tokens (int): Maximum tokens in the response.

    Returns:
        str: The LLM-generated response as a string.
    """
    if not OPENAI_API_KEY:
        logger.error("OpenAI API Key not set. Cannot call LLM.")
        return ""

    openai.api_key = OPENAI_API_KEY

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

# palm.configure(api_key=GEMINI_API_KEY)

# def call_gemini(prompt: str, model: str = "models/chat-bison-001", temperature: float = 0.0, max_output_tokens: int = 200) -> str:
#     """Call the Gemini API."""
#     try:
#         response = palm.generate_text(
#             model=model,
#             prompt=prompt,
#             temperature=temperature,
#             max_output_tokens=max_output_tokens
#         )

#         if response.result:
#             output = response.result
#             logger.debug(f"Gemini response: {output}")
#             return output
#         else:
#             logger.warning("Gemini response was empty.")
#             return ""

#     except Exception as e:
#         logger.exception(f"Gemini call failed: {e}")  # Log the full exception details
#         return ""

# def call_llm(prompt: str, model: str = "models/chat-bison-001", max_output_tokens: int = 200) -> str:
#     return call_gemini(prompt, model, max_output_tokens)

def infer_schema_with_llm(sample_rows, model: str = "gpt-4o-mini") -> str:
# def infer_schema_with_llm(sample_rows, model: str = "models/chat-bison-001") -> str:
    """
    Prompt the LLM to suggest headers/column names for a table without headers.

    Args:
        sample_rows (list): List of lists representing rows of data.
        model (str): Which model to use.

    Returns:
        str: JSON-encoded list of suggested column headers (if successful).
    """
    prompt = f"""
The following data rows do not have headers:
{sample_rows}

Suggest likely column headers (one per column), and return ONLY a JSON list of strings.
For example: ["ID", "Name", "Date", "Amount"].
"""
    schema_suggestion = call_llm(prompt, model=model, max_tokens=3000)
    # schema_suggestion = call_llm(prompt, model=model, max_output_tokens=200)
    # schema_suggestion = call_llm(prompt, model=model)
    return schema_suggestion
    # return schema_suggestion

def summarize_text_with_llm(cleaned_text: str, model: str = "gpt-4o-mini") -> str:
# def summarize_text_with_llm(cleaned_text: str, model: str = "models/chat-bison-001") -> str:
    """
    Summarize large text using an LLM.

    Args:
        cleaned_text (str): Preprocessed text.
        model (str): Which model to use.

    Returns:
        str: Summary text.
    """
    if len(cleaned_text) < 10:
        return "No meaningful text to summarize."

    prompt = f"""
Summarize the following text in a concise, high-level manner:
{cleaned_text}
"""
    summary = call_llm(prompt, model=model, max_tokens=3000)
    # summary = call_llm(prompt, model=model)
    return summary

def generate_data_insights_with_llm(df, model: str = "gpt-4o-mini") -> str:
# def generate_data_insights_with_llm(df, model: str = "models/chat-bison-001") -> str: 
    """
    Provide a high-level analysis of a DataFrame using an LLM.

    Args:
        df (pd.DataFrame): DataFrame to analyze.
        model (str): Which model to use.

    Returns:
        str: Text of data insights.
    """
    if df.empty:
        return "No data available for analysis."

    # Convert a small portion of the data to CSV or JSON for context
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
    # analysis = call_llm(prompt, model=model)
    return analysis