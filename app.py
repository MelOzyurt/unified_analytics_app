# app.py

import streamlit as st

# --- App Config ---
st.set_page_config(page_title="Unified Analytics App", layout="wide")

# --- Import Modules ---
from auth.session import init_session_state, reset_session
from auth.login import login_ui
from components.sidebar import show_sidebar
from components.cost_panel import show_cost_panel
from upload.file_handler import upload_and_process_file
from analysis.analyze_data import analyze_data_ui
from analysis.analyze_feedback import analyze_feedback_ui
from analysis.chat_with_doc import chat_with_doc_ui

# --- Initialize session state ---
init_session_state()


def main():
    st.title("📊 Unified Analytics Platform")

    # Show sidebar (user info & logout)
    show_sidebar()

    # Show login screen if not logged in
    if not st.session_state.get("logged_in", False):
        login_ui()
        return

    # --- Upload Section ---
    st.header("📁 Upload Your Data")
    uploaded_data, file_type = upload_and_process_file()

    if uploaded_data is None:
        st.info("Please upload your data to proceed.")
        return

    st.success(f"✅ File uploaded successfully! Detected type: `{file_type}`")
    st.dataframe(uploaded_data.head())
    st.session_state["uploaded_data"] = uploaded_data

    # --- Analysis Type ---
    st.subheader("🧠 Choose Analysis Type")
    analysis_type = st.radio(
        "Select one of the following analysis options:",
        ["Analyze Data", "Analyze Feedback", "Chat With Document"]
    )
    st.session_state["analysis_type"] = analysis_type

    # --- Cost Panel ---
    show_cost_panel(analysis_type)

    # --- Run Button ---
    if st.button("🚀 Run Analysis"):
        if st.session_state.balance <= 0:
            st.error("❌ Insufficient balance. Please top up your account.")
            return

        if analysis_type == "Analyze Data":
            analyze_data_ui(uploaded_data)

        elif analysis_type == "Analyze Feedback":
            analyze_feedback_ui(uploaded_data)

        elif analysis_type == "Chat With Document":
            chat_with_doc_ui(uploaded_data)

        else:
            st.warning("⚠️ Invalid selection.")

# --- App Runner ---
if __name__ == "__main__":
    main()
