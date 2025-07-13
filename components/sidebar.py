# components/sidebar.py

import streamlit as st
from auth.session import reset_session

def show_sidebar():
    with st.sidebar:
        st.title("👤 Account")

        if st.session_state.get("logged_in"):
            st.markdown(f"**User:** `{st.session_state.username}`")
            st.markdown(f"**Balance:** ${st.session_state.balance:.2f}")

            if st.button("🚪 Logout"):
                reset_session()
                st.success("Logged out successfully.")
                st.experimental_rerun()

        else:
            st.info("Please log in from the main page.")

        st.markdown("---")

        st.caption("💡 Tip: You can top up your balance later.")
