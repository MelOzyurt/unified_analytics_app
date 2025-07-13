# app.py

import streamlit as st
from auth.session import init_session_state
from auth.login import login_ui
from components.sidebar import show_sidebar
from components.cost_panel import show_cost_panel
from upload.file_handler import upload_and_process_file
from analysis.analyze_data import analyze_data_ui   # ✅ doğru fonksiyon ismiyle düzeltildi
from analysis.analyze_feedback import analyze_feedback_ui
from analysis.chat_with_doc import chat_with_doc_ui
from analysis.analyze_data_ai import analyze_data_ai_ui
from payment.deposit import deposit_ui

# App Configuration
st.set_page_config(page_title="Unified Analytics App", layout="wide")
init_session_state()

def main():
    st.title("📊 Unified Analytics Platform")

    # Sidebar (User Info, Logout)
    show_sidebar()

    # Login Flow
    if not st.session_state.get("logged_in", False):
        login_ui()
        return

    # Deposit Section
    with st.expander("💳 Deposit Funds to Account"):
        deposit_ui()

    # File Upload
    st.header("📁 Upload Your Data")
    uploaded_data, file_type = upload_and_process_file()

    if uploaded_data is None:
        st.info("Please upload a valid file to continue.")
        return

    st.success(f"✅ File uploaded successfully! Format: `{file_type}`")
    st.dataframe(uploaded_data.head())
    st.session_state["uploaded_data"] = uploaded_data

    # Analysis Selection
    st.subheader("🧠 Choose Analysis Type")
    analysis_type = st.radio(
        "Select an option:",
        [
            "Analyze Data (Classic)",
            "Analyze Data (AI-Assisted)",
            "Analyze Feedback",
            "Chat With Document"
        ]
    )
    st.session_state["analysis_type"] = analysis_type

    # Cost Panel
    show_cost_panel(analysis_type)

    # Run Analysis
    if st.button("🚀 Run Analysis"):
        if st.session_state.balance <= 0:
            st.error("❌ Insufficient balance. Please deposit funds.")
            return

        # Route to appropriate analysis
        if analysis_type == "Analyze Data (Classic)":
            analyze_data_ui(uploaded_data)

        elif analysis_type == "Analyze Data (AI-Assisted)":
            analyze_data_ai_ui(uploaded_data)

        elif analysis_type == "Analyze Feedback":
            analyze_feedback_ui(uploaded_data)

        elif analysis_type == "Chat With Document":
            chat_with_doc_ui(uploaded_data)

        else:
            st.warning("⚠️ Invalid analysis type selected.")

# Entry point
if __name__ == "__main__":
    main()
