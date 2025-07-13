import streamlit as st
import pandas as pd

def handle_file_upload():
    st.subheader("Upload your data")
    uploaded_file = st.file_uploader("Upload Excel, CSV, JSON, PDF, DOCX", 
                                     type=["xlsx", "csv", "json", "pdf", "docx"])
    if uploaded_file is not None:
        # Simple example: if CSV or Excel, read as DataFrame
        if uploaded_file.type in ["text/csv", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
            try:
                if uploaded_file.type == "text/csv":
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                st.success("Data loaded successfully!")
                return df
            except Exception as e:
                st.error(f"Failed to read spreadsheet: {e}")
                return None
        else:
            # For PDF, DOCX or other formats, return raw bytes or text for chat
            data = uploaded_file.read()
            st.success("File uploaded successfully!")
            return data
    else:
        return None
