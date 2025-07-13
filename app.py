import streamlit as st
from components.sidebar import show_sidebar
from auth.login import login_ui
from data_upload import upload_data_ui
from analysis.analyze_data import analyze_data_ui
from analysis.analyze_feedback import analyze_feedback_ui
from chat.chat_with_doc import chat_with_doc_ui

def main():
    st.set_page_config(page_title="Unified Analytics App")

    # Show sidebar and get user's choice
    app_mode = show_sidebar()

    # Check login state
    if not st.session_state.get("logged_in", False):
        login_ui()
        return

    # After login, show data upload section
    df = upload_data_ui()

    # If no data uploaded, ask user
    if df is None:
        st.info("Please upload your data to continue.")
        return

    # Depending on sidebar choice, call the corresponding UI
    if app_mode == "Analyze Data":
        analyze_data_ui(df)
    elif app_mode == "Analyze Feedback":
        analyze_feedback_ui(df)
    elif app_mode == "Chat with Document":
        chat_with_doc_ui(df)

if __name__ == "__main__":
    main()
