import streamlit as st
import json
import hashlib
import os
import analyse_functions as af
from trainer_app import get_color_for_hit_rate

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

    

    st.markdown("---")  # Trennlinie zwischen den Athleten

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
           

            # Lade die Statistiken des Athleten
            statistics_file = f"JSON/biathlon_statistics_K_{user['first_name']}_{user['last_name']}.json"
            try:
                with open(statistics_file, 'r') as file:
                    statistics = json.load(file)
                total_shots = af.calculate_total_shots(statistics)
                total_prone_errors = af.calculate_prone_errors(statistics)
                total_standing_errors = af.calculate_standing_errors(statistics)
                overall_hit_rate, prone_hit_rate, standing_hit_rate = af.calculate_hit_rate(total_shots, total_prone_errors, total_standing_errors)

                st.write(f"Total Shots: {total_shots}")
                st.write(f"Total Errors: {total_prone_errors + total_standing_errors}")
            except FileNotFoundError:
                st.write("No statistics available for this athlete.")
                total_shots = None
                total_prone_errors = None
                total_standing_errors = None
                overall_hit_rate = None
                prone_hit_rate = None
                standing_hit_rate = None
    with col2:
        if overall_hit_rate is not None:
            st.write(f"Overall Hit Rate: {overall_hit_rate:.2%}")
            st.write(f"Prone Hit Rate: {prone_hit_rate:.2%}")
            st.write(f"Standing Hit Rate: {standing_hit_rate:.2%}")
        else:
            st.write("No hit rate data available.")
    with col3:
        if overall_hit_rate is not None:
            st.markdown(f"<div style='width: 30px; height: 30px; background-color: {get_color_for_hit_rate(overall_hit_rate)}'></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='width: 30px; height: 30px; background-color: {get_color_for_hit_rate(prone_hit_rate)}'></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='width: 30px; height: 30px; background-color: {get_color_for_hit_rate(standing_hit_rate)}'></div>", unsafe_allow_html=True)
        else:
            st.write("")
  


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