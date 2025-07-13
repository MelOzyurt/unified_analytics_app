# auth/login.py

import streamlit as st
import json
import hashlib
import os

USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists."
    users[username] = hash_password(password)
    save_users(users)
    return True, "User registered successfully."

def login_user(username, password):
    users = load_users()
    hashed = hash_password(password)
    return username in users and users[username] == hashed

def login_ui():
    with st.sidebar:
        st.markdown("#### 🔐 Access")
        tab = st.radio(
            label="Select Action",
            options=["Login", "Register"],
            horizontal=True,
            label_visibility="hidden"
)


        if tab == "Login":
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("✅ Login"):
                if login_user(username, password):
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.success(f"Welcome, {username}!")
                else:
                    st.error("❌ Invalid credentials.")

        else:
            username = st.text_input("Username", key="reg_user")
            password = st.text_input("Password", type="password", key="reg_pass")
            if st.button("📝 Register"):
                ok, msg = register_user(username, password)
                st.success(msg) if ok else st.error(msg)

def is_logged_in():
    return st.session_state.get("logged_in", False)
