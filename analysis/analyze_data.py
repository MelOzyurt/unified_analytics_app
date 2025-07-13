# analysis/analyze_data.py

import streamlit as st
import pandas as pd

def analyze_data_ui(df: pd.DataFrame):
    st.header("📊 Classic Data Analysis")

    if df is None or df.empty:
        st.warning("No data available for analysis.")
        return

    st.subheader("Data Preview")
    st.dataframe(df.head())

    st.subheader("Descriptive Statistics")
    st.write(df.describe())

    st.subheader("Data Info")
    buffer = []
    df.info(buf=buffer)
    info_str = "\n".join(buffer)
    st.text(info_str)

    st.subheader("Columns")
    st.write(df.columns.tolist())
