

---

# **Metadata Extractor: LLM-Enhanced Data Abstraction**

## **Project Overview**

The **Metadata Extractor** is an automated solution designed to:

- Detect and parse multiple file types (**TXT**, **CSV**, **XLSX**, **PDF**).  
- Preprocess the extracted data (cleaning text, handling missing headers in Excel).  
- Use **Large Language Models (LLMs)** for:
  - **Schema inference** (suggesting column names).  
  - **Summarizing unstructured text**.  
  - **Generating insights** from structured data.  
- Output **structured metadata** and **high-level summaries or insights** in **JSON** or optionally in **Excel**.

**Key Features**

- **Multi-Format Support**  
  Text, Excel, CSV, and PDF ingestion in a single pipeline.  
- **LLM Integration**  
  Utilizes GPT-based models (e.g., GPT-3.5 or GPT-4) for schema inference, text summarization, and data insights.  
- **Schema Detection**  
  Infers column names for Excel/CSV files with missing headers.  
- **Scalable Design**  
  Modular code structure allows easy extension to new file types or advanced NLP steps.  
- **Streamlit UI**  
  Provides an **interactive** interface for multi-file uploads, metadata viewing, and LLM-driven summaries.

---

## **Setup Instructions**

### **Prerequisites**

- **Python 3.8+**  
- **pip** (Python package manager)  
- **OpenAI API Key** (for LLM integration)  

### **Clone the Repository**

```bash
git clone https://github.com/ShantamShukla/Metadata-Extractor.git
cd metadata-extractor
```

### **Create and Activate Virtual Environment**

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Linux/macOS
source venv/bin/activate
```

### **Install Dependencies**

```bash
pip install -r requirements.txt
```

### **Environment Variables**

Create a file named `.env` in the project root:

```
OPENAI_API_KEY=your_openai_api_key_here
```

---

## **Running the Application**

### **Command Line (CLI)**

```bash
python main.py --input-file /path/to/your/file
```

- **Supported file types**: `.txt`, `.csv`, `.xlsx`, `.pdf`  
- Output is **structured JSON** containing metadata, suggested schema (if any), and/or summarized insights.

### **Streamlit App**

For a **multi-file** upload experience with a **visual interface**:

```bash
streamlit run app.py
```

1. Drag and drop up to 15 files (`.pdf`, `.txt`, `.csv`, `.xlsx`).  
2. View file **metadata** (size, type, row/column counts, PDF pages, etc.).  
3. See LLM-based **summaries** (entire document or short chapter-based) and **schema suggestions** for Excel/CSV files.  

---

## **Output Format**

The pipeline produces a **JSON** structure containing:

- **File metadata** (rows, columns, sample data, page counts, etc.)  
- **Suggested schema** (if applicable for Excel/CSV)  
- **Summarized text** (PDF/TXT) or **data insights** (Excel/CSV)

### **Example** (Excel)

![Result](Screenshots%20of%20result/Screenshot%202025-02-06%20210619.png)

---

## **Contact**

For questions or suggestions, please **open an issue** in the [GitHub repository](https://github.com/ShantamShukla/Metadata-Extractor).

---

### **Enjoy using the Metadata Extractor!** Feel free to enhance it with additional NLP features or integrate it into your data processing pipelines.