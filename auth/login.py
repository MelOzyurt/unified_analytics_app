# auth/login.py

import streamlit as st

# Simple in-memory user store (for demo/testing)
DEMO_USERS = {
    "demo": "password123",
    "admin": "adminpass"
}

def login_ui():
    st.subheader("🔐 Please Log In")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in DEMO_USERS and DEMO_USERS[username] == password:
            st.success(f"Welcome back, {username}!")
            st.session_state.logged_in = True
            st.session_state.username = username

            # Set a default balance if first time login
            if "balance" not in st.session_state:
                st.session_state.balance = 50.0

        else:
            st.error("Invalid username or password.")

    st.markdown("Don't have an account? Use demo/demo123 or admin/adminpass for now.")
