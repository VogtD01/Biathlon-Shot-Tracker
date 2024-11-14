import streamlit as st
import json
import hashlib

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

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Profile page
def profile_page():
    st.title("Profile")

    if 'user' not in st.session_state:
        st.error("You need to log in to view this page.")
        return

    user = st.session_state.user

    st.write(f"Logged in as: {user['email']}")

    st.subheader("Update Profile Information")

    first_name = st.text_input("First Name", value=user['first_name'])
    last_name = st.text_input("Last Name", value=user['last_name'])
    email = st.text_input("Email", value=user['email'])
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Update Profile"):
        if not first_name or not last_name or not email:
            st.error("All fields are required!")
        elif password and password != confirm_password:
            st.error("Passwords do not match!")
        else:
            users = load_users()
            for u in users:
                if u['email'] == user['email']:
                    u['first_name'] = first_name
                    u['last_name'] = last_name
                    u['email'] = email
                    if password:
                        u['password'] = hash_password(password)
                    break
            save_users(users)
            st.session_state.user = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": user['password'] if not password else hash_password(password)
            }
            st.success("Profile updated successfully!")

    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.experimental_rerun()