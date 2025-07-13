# analysis/analyze_feedback.py

import streamlit as st
import pandas as pd
import re
from textblob import TextBlob
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

def analyze_feedback_ui(data):
    st.header("📝 Analyze Customer Feedback")

    # Accept either raw text or a dataframe with text columns
    if isinstance(data, pd.DataFrame):
        text_cols = data.select_dtypes(include=['object']).columns.tolist()
        if not text_cols:
            st.error("No text columns found in data for feedback analysis.")
            return

        col = st.selectbox("Select text column for analysis", text_cols)
        all_text = " ".join(data[col].dropna().astype(str).tolist())
    elif isinstance(data, str):
        all_text = data
    else:
        st.error("Unsupported data type for feedback analysis.")
        return

    if not all_text.strip():
        st.warning("No feedback text found.")
        return

    cleaned_text = clean_text(all_text)

    # Sentiment Analysis
    st.subheader("Sentiment Analysis")
    blob = TextBlob(cleaned_text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    st.write(f"**Polarity:** {polarity:.3f} (Negative < 0 < Positive)")
    st.write(f"**Subjectivity:** {subjectivity:.3f} (Objective 0 - Subjective 1)")

    # Word Frequency
    st.subheader("Common Words & Word Cloud")
    words = cleaned_text.split()
    word_counts = Co_
