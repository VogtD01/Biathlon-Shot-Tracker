import streamlit as st
import json
import hashlib
import os

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

    col1, col2 = st.columns([1, 2])

    with col1:
         image_path = f"images/{user['email']}.jpg"
         if os.path.exists(image_path):
            st.image(image_path, width=150)
         else:
            st.image("images/default.jpg", width=150)

    with col2:
        st.write(f"**First Name:** {user['first_name']}")
        st.write(f"**Last Name:** {user['last_name']}")
        st.write(f"**Gender:** {user.get('gender', 'Male')}")
        st.write(f"**Height:** {user.get('height', 0)} cm")
        st.write(f"**Weight:** {user.get('weight', 0)} kg")

    with st.expander("Update Profile Information"):
        st.subheader("Update Profile Information")

        first_name = st.text_input("First Name", value=user['first_name'])
        last_name = st.text_input("Last Name", value=user['last_name'])
        height = st.number_input("Height (cm)", value=user.get('height', 0))
        weight = st.number_input("Weight (kg)", value=user.get('weight', 0))
        email = st.text_input("Email", value=user['email'])
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        uploaded_file = st.file_uploader("Upload a new profile picture", type=["jpg", "jpeg", "png"])

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
                        u['height'] = height
                        u['weight'] = weight
                        u['email'] = email
                        if password:
                            u['password'] = hash_password(password)
                        break
                save_users(users)
                st.session_state.user = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "height": height,
                    "weight": weight,
                    "email": email,
                    "password": user['password'] if not password else hash_password(password)
                }
                if uploaded_file is not None:
                    with open(f"images/{email}.jpg", "wb") as f:
                        f.write(uploaded_file.getbuffer())
                st.success("Profile updated successfully!")

    st.write(f"Logged in as: {user['email']}")

    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()