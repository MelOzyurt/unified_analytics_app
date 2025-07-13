import streamlit as st
import pandas as pd

SUPPORTED_FILE_TYPES = {
    "csv": "CSV",
    "xlsx": "Excel",
    "xls": "Excel",
    "json": "JSON",
    "xml": "XML",
    "feather": "Feather"
}

def upload_and_process_file():
    uploaded_file = st.file_uploader(
        "Upload your dataset (CSV, Excel, JSON, XML, Feather)",
        type=list(SUPPORTED_FILE_TYPES.keys())
    )

    if uploaded_file is None:
        return None, None

    try:
        file_type = uploaded_file.name.split(".")[-1].lower()

        if file_type == "csv":
            df = pd.read_csv(uploaded_file)
        elif file_type in ["xlsx", "xls"]:
            df = pd.read_excel(uploaded_file)
        elif file_type == "json":
            df = pd.read_json(uploaded_file)
        elif file_type == "xml":
            df = pd.read_xml(uploaded_file)
        elif file_type == "feather":
            df = pd.read_feather(uploaded_file)
        else:
            st.error("❌ Unsupported file format.")
            return None, None

        return df, SUPPORTED_FILE_TYPES[file_type]

    except Exception as e:
        st.error(f"❌ Failed to read file: {e}")
        return None, None
