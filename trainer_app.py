import streamlit as st
from streamlit_option_menu import option_menu
import json
import os
import matplotlib.pyplot as plt
import analyse_page as ap

# Load athletes from a JSON file
def load_athletes():
    with open('users.json', 'r') as file:
        users = json.load(file)
        # Filter out users with the first name "Trainer"
        athletes = [user for user in users if user['first_name'].lower() != 'trainer']
        return athletes

# Save the trainer's team to a JSON file
def save_trainer_team(trainer_team, trainer_name):
    filename = f"{trainer_name}_team.json"
    with open(filename, 'w') as file:
        json.dump(trainer_team, file, indent=4)

# Load the trainer's team from a JSON file
def load_trainer_team(trainer_name):
    filename = f"{trainer_name}_team.json"
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def trainer_app():
    st.title("Welcome, Trainer " + st.session_state.user['last_name'] + "!")

    # Check if the logged-in user is Trainer Huber
    if st.session_state.user['first_name'].lower() == 'trainer' and st.session_state.user['last_name'].lower() == 'huber':

        trainer_name = f"{st.session_state.user['first_name'].lower()}_{st.session_state.user['last_name'].lower()}"

        # Load the trainer's team from the JSON file
        if 'trainer_team' not in st.session_state:
            st.session_state.trainer_team = load_trainer_team(trainer_name)

        # Page navigation
        selected = option_menu(
            menu_title=None,
            options=['My Team', 'Statistics/Graphs', 'Team Manager'],
            icons=['person-standing', 'graph-up', 'person-fill-gear'],
            default_index=0,
            orientation='horizontal'
        )

        if selected == 'My Team':
            show_team()
        elif selected == 'Statistics/Graphs':
            show_stats()
        elif selected == 'Team Manager':
            team_management(trainer_name)
    else:
        st.error("You are not authorized to access this page.")

def show_team():
    if 'trainer_team' in st.session_state and st.session_state.trainer_team:
         for athlete in st.session_state.trainer_team:
            image_path = f"images/{athlete['email']}.jpg"
            if os.path.exists(image_path):
                st.image(image_path, width=100)
            else:
                st.image("images/default.jpg", width=100)
            st.write(f"{athlete['first_name']} {athlete['last_name']}")
    else:
        st.write("No athletes in your team yet.")

def show_stats():
     if 'trainer_team' in st.session_state and st.session_state.trainer_team:
        athlete_names = [f"{athlete['first_name']} {athlete['last_name']}" for athlete in st.session_state.trainer_team]
        selected_athlete_name = st.selectbox("Select Athlete", athlete_names)

        selected_athlete = next((athlete for athlete in st.session_state.trainer_team if f"{athlete['first_name']} {athlete['last_name']}" == selected_athlete_name), None)

        if selected_athlete:
            st.write(f"Showing stats for {selected_athlete['first_name']} {selected_athlete['last_name']}")

            ap.main(selected_athlete)
        else:
            st.write("No stats available for the selected athlete.")
     else:
        st.write("No athletes in your team yet.")

def team_management(trainer_name):
    # Load all athletes
    athletes = load_athletes()

    # Filter out athletes who are already in the trainer's team
    available_athletes = [athlete for athlete in athletes if athlete not in st.session_state.trainer_team]

    # Select athletes for the trainer's team
    st.subheader("Select Athletes for Your Team")
    selected_athletes = st.multiselect(
        "Select Athletes",
        options=[f"{athlete['first_name']} {athlete['last_name']}" for athlete in available_athletes]
    )

    # Save the selected athletes to the trainer's team
    if st.button("Save Team"):
        trainer_team = [athlete for athlete in athletes if f"{athlete['first_name']} {athlete['last_name']}" in selected_athletes]
        st.session_state.trainer_team.extend(trainer_team)
        save_trainer_team(st.session_state.trainer_team, trainer_name)
        st.success("Team saved successfully!")

    # Select athletes to remove from the trainer's team
    st.subheader("Remove Athletes from Your Team")
    selected_athletes_to_remove = st.multiselect(
        "Select Athletes to Remove",
        options=[f"{athlete['first_name']} {athlete['last_name']}" for athlete in st.session_state.trainer_team]
    )

    # Remove the selected athletes from the trainer's team
    if st.button("Remove Selected Athletes"):
        st.session_state.trainer_team = [athlete for athlete in st.session_state.trainer_team if f"{athlete['first_name']} {athlete['last_name']}" not in selected_athletes_to_remove]
        save_trainer_team(st.session_state.trainer_team, trainer_name)
        st.success("Selected athletes removed successfully!")

# Example users.json content:
# [
#     {"first_name": "John", "last_name": "Doe", "image_url": "path/to/john_doe_image.png"},
#     {"first_name": "Jane", "last_name": "Smith", "image_url": "path/to/jane_smith_image.png"},
#     {"first_name": "Emily", "last_name": "Jones", "image_url": "path/to/emily_jones_image.png"},
#     {"first_name": "Trainer", "last_name": "Huber", "image_url": "path/to/trainer_huber_image.png"}
# ]

# Example trainer_huber_team.json content:
# [
#     {"first_name": "John", "last_name": "Doe", "image_url": "path/to/john_doe_image.png"},
#     {"first_name": "Jane", "last_name": "Smith", "image_url": "path/to/jane_smith_image.png"}
# ]

if __name__ == "__main__":
    trainer_app()