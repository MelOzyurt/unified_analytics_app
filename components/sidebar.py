# components/sidebar.py

import streamlit as st
from auth.session import reset_session

def show_sidebar():
    with st.sidebar:
        st.markdown("#### 👤 Account", unsafe_allow_html=True)

        if st.session_state.get("logged_in"):
            st.markdown(f"- **User:** `{st.session_state.username}`")
            st.markdown(f"- **Balance:** `${st.session_state.balance:.2f}`")
            if st.button("🚪 Logout"):
                reset_session()
                st.success("Logged out.")
                st.experimental_rerun()
        else:
            st.caption("Tip: Balance top-up is available after login.")
