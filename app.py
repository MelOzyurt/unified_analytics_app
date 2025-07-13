# app.py

import streamlit as st
from auth.session import init_session_state
from auth.login import login_ui
from components.sidebar import show_sidebar
from upload.file_handler import upload_and_process_file
from analysis.analyze_data import analyze_data_ui
from analysis.analyze_feedback import analyze_feedback_ui
from analysis.chat_with_doc import chat_with_doc_ui
from analysis.analyze_data_ai import analyze_data_ai_ui
from payment.deposit import deposit_ui

# Page setup
st.set_page_config(page_title="Unified Analytics App", layout="wide")

# Initialize session state
init_session_state()

def main():
    # Sidebar with account info
    show_sidebar()

    # Login screen
    if not st.session_state.get("logged_in", False):
        login_ui()
        return

    # Main content after login
    st.title("📊 Unified Analytics Platform")
    st.write("🎉 Login successful!")

    # Deposit section
    with st.expander("💳 Deposit Funds to Your Account"):
        deposit_ui()

    # File upload
    st.header("📁 Upload Your Data File")
    uploaded_data, file_type = upload_and_process_file()

    if uploaded_data is None:
        st.info("Please upload a file to proceed.")
        return

    st.success(f"File uploaded successfully! Format: `{file_type}`")
    st.dataframe(uploaded_data.head())

    # Analysis type selection
    st.subheader("🧠 Select Analysis Type")
    analysis_type = st.radio(
        "Choose an analysis option:",
        [
            "Analyze Data (Classic)",
            "Analyze Data (AI-Assisted)",
            "Analyze Feedback",
            "Chat With Document"
        ]
    )

    # Run analysis
    if st.button("🚀 Run Analysis"):
        if st.session_state.balance <= 0:
            st.error("❌ Insufficient balance. Please deposit funds first.")
            return

        if analysis_type == "Analyze Data (Classic)":
            analyze_data_ui(uploaded_data)
        elif analysis_type == "Analyze Data (AI-Assisted)":
            analyze_data_ai_ui(uploaded_data)
        elif analysis_type == "Analyze Feedback":
            analyze_feedback_ui(uploaded_data)
        elif analysis_type == "Chat With Document":
            chat_with_doc_ui(uploaded_data)
        else:
            st.warning("⚠️ Unknown analysis type.")

# Entry point
if __name__ == "__main__":
    main()
