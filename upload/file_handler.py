# upload/file_handler.py

import streamlit as st
import pandas as pd
import json
import io

from PyPDF2 import PdfReader
import docx
import pyarrow.feather as feather


def upload_and_process_file():
    """
    Handles file upload and processes it based on file type.
    Returns (dataframe_or_text, file_type)
    """
    uploaded_file = st.file_uploader(
        "Upload file (CSV, Excel, JSON, PDF, DOCX, TXT, Feather)", 
        type=["csv", "xlsx", "xls", "json", "pdf", "docx", "txt", "feather"]
    )

    if uploaded_file is not None:
        file_type = uploaded_file.type

        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
                return df, "csv"

            elif uploaded_file.name.endswith((".xlsx", ".xls")):
                df = pd.read_excel(uploaded_file)
                return df, "excel"

            elif uploaded_file.name.endswith(".json"):
                data = json.load(uploaded_file)
                df = pd.json_normalize(data)
                return df, "json"

            elif uploaded_file.name.endswith(".feather"):
                df = feather.read_feather(uploaded_file)
                return df, "feather"

            elif uploaded_file.name.endswith(".pdf"):
                reader = PdfReader(uploaded_file)
                text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
                return text, "pdf"

            elif uploaded_file.name.endswith(".docx"):
                doc = docx.Document(uploaded_file)
                text = "\n".join([para.text for para in doc.paragraphs])
                return text, "docx"

            elif uploaded_file.name.endswith(".txt"):
                text = uploaded_file.read().decode("utf-8")
                return text, "txt"

            else:
                st.warning("Unsupported file format.")
                return None, None

        except Exception as e:
            st.error(f"❌ Error processing file: {e}")
            return None, None

    return None, None
