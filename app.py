import streamlit as st
from login import login_ui, is_logged_in
from sidebar import sidebar_ui
from cost_panel import show_cost_panel
from file_handler import handle_file_upload
from analysis.analyze_data import analyze_data_ui
from analysis.analyze_feedback import analyze_feedback_ui
from analysis.chat_with_doc import chat_with_doc_ui

# --- Login First ---
login_ui()

if not is_logged_in():
    st.stop()

# --- Main App (after login) ---
st.title(f"📊 Unified Analytics App — Welcome {st.session_state['username']}")

# Sidebar UI (app navigation)
app_mode = sidebar_ui()

# Cost panel on right
show_cost_panel()

# File upload area
uploaded_data = handle_file_upload()

# Show analysis options only if file uploaded
if uploaded_data:
    if app_mode == "Analyze Data":
        analyze_data_ui(uploaded_data)
    elif app_mode == "Analyze Feedback":
        analyze_feedback_ui(uploaded_data)
    elif app_mode == "Chat with Document":
        chat_with_doc_ui(uploaded_data)
else:
    st.warning("⬆️ Please upload your file to begin.")
