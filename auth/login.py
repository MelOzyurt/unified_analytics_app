# login.py

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
    if username in users and users[username] == hashed:
        return True
    return False

def login_ui():
    st.sidebar.subheader("🔐 Login or Register")

    tab = st.sidebar.radio("Choose", ["Login", "Register"])

    if tab == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            if login_user(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success(f"Welcome, {username}!")
            else:
                st.error("Invalid username or password.")

    elif tab == "Register":
        username = st.sidebar.text_input("New Username")
        password = st.sidebar.text_input("New Password", type="password")
        if st.sidebar.button("Register"):
            ok, msg = register_user(username, password)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

def is_logged_in():
    return st.session_state.get("logged_in", False)
