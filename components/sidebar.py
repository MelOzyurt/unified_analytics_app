# components/sidebar.py

import streamlit as st
from auth.session import reset_session
from streamlit.runtime.scriptrunner import rerun  # ✅ EKLE

def show_sidebar():
    with st.sidebar:
        st.markdown("#### 👤 Account")

        if st.session_state.get("logged_in"):
            st.markdown(f"- **User:** `{st.session_state.username}`")
            st.markdown(f"- **Balance:** `${st.session_state.balance:.2f}`")
            if st.button("🚪 Logout"):
                reset_session()
                st.success("Logged out.")
                rerun()  # ✅ GÜNCEL
        else:
            st.caption("Tip: Balance top-up is available after login.")
