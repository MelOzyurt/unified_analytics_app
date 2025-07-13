# auth/session.py

import streamlit as st

def init_session_state():
    """
    Initializes default session state values if not already set.
    """
    default_state = {
        "logged_in": False,
        "username": None,
        "balance": 50.0,
        "uploaded_data": None,
        "file_type": None,
        "analysis_type": None,
        "last_analysis_result": None,
    }

    for key, value in default_state.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_session():
    """
    Resets all session variables to defaults (e.g., on logout).
    """
    keys_to_reset = [
        "logged_in", "username", "balance",
        "uploaded_data", "file_type", "analysis_type", "last_analysis_result"
    ]

    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]
