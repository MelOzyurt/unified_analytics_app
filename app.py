import streamlit as st
from login import login_ui, is_logged_in
from sidebar import sidebar_ui
from cost_panel import show_cost_panel
from file_handler import handle_file_upload
from analysis.analyze_data import analyze_data_ui
from analysis.analyze_feedback import analyze_feedback_ui
from analysis.chat_with_doc import chat_with_doc_ui

def main():
    # Run login UI and check
    login_ui()
    if not is_logged_in():
        st.warning("Please log in to use the app.")
        st.stop()

    st.title(f"📊 Unified Analytics App — Welcome {st.session_state['username']}")

    # Sidebar for choosing main app mode
    app_mode = sidebar_ui()

    # Show cost panel on right
    show_cost_panel()

    # File upload section
    uploaded_data = handle_file_upload()

    if uploaded_data:
        # Depending on mode, show corresponding analysis UI
        if app_mode == "Analyze Data":
            analyze_data_ui(uploaded_data)
        elif app_mode == "Analyze Feedback":
            analyze_feedback_ui(uploaded_data)
        elif app_mode == "Chat with Document":
            chat_with_doc_ui(uploaded_data)
        else:
            st.info("Please select an analysis mode from the sidebar.")
    else:
        st.info("Please upload a data file to proceed.")

if __name__ == "__main__":
    main()
