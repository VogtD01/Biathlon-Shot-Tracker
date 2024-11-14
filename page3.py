import streamlit as st
import json
import hashlib

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to load user data
def load_users():
    try:
        with open('users.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save user data
def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None

# Login page
def login_page():
    st.title("User Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = load_users()
        user = next((user for user in users if user['email'] == email), None)
        if user is None:
            st.error("Email not registered!")
        else:
            hashed_login_password = hash_password(password)
            if user['password'] == hashed_login_password:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Incorrect password!")

    if st.button("Registration"):
        st.session_state.page = 'register'
        st.rerun()

# Registration page
def registration_page():
    st.title("User Registration")

    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if not first_name or not last_name or not email or not password or not confirm_password:
            st.error("All fields are required!")
        elif password != confirm_password:
            st.error("Passwords do not match!")
        else:
            users = load_users()
            if any(user['email'] == email for user in users):
                st.error("Email already registered!")
            else:
                hashed_password = hash_password(password)
                new_user = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "password": hashed_password
                }
                users.append(new_user)
                save_users(users)
                st.success("Registration successful! You can now log in.")
                st.session_state.page = 'login'
                st.rerun()

    if st.button("Go to Login"):
        st.session_state.page = 'login'
        st.rerun()

# Welcome page
def welcome_page():
    st.title(f"Welcome, {st.session_state.user['first_name']} {st.session_state.user['last_name']}!")

# Page navigation
if 'page' not in st.session_state:
    st.session_state.page = 'login'

if st.session_state.logged_in:
    welcome_page()
else:
    if st.session_state.page == 'login':
        login_page()
    elif st.session_state.page == 'register':
        registration_page()