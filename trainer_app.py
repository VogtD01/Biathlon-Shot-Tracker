import streamlit as st
from streamlit_option_menu import option_menu
import json
import os
import matplotlib.pyplot as plt
import analyse_page as ap
import analyse_functions as af

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



def get_color_for_hit_rate(hit_rate):
    if hit_rate < 0.5:
        red = 255
        green = 0
    elif hit_rate < 0.85:
        red = 255
        green = int(255 * ((hit_rate - 0.5) / 0.35))
    else:
        red = 0
        green = int(255 * ((1 - hit_rate) / 0.15))
        green = max(green, 128)  # Ensure green is at least 128 for 100%
    return f"rgb({red}, {green}, 0)"

def show_team():
    if 'trainer_team' in st.session_state and st.session_state.trainer_team:
        for athlete in st.session_state.trainer_team:
            col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
            with col1:
                image_path = f"images/{athlete['email']}.jpg"
                if os.path.exists(image_path):
                    st.image(image_path, width=100)
                else:
                    st.image("images/default.jpg", width=100)
            with col2:
                st.write(f"{athlete['first_name']} {athlete['last_name']}")

                # Lade die Statistiken des Athleten
                statistics_file = f"JSON/biathlon_statistics_K_{athlete['first_name']}_{athlete['last_name']}.json"
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
            with col3:
                if overall_hit_rate is not None:
                    st.write(f"Overall Hit Rate: {overall_hit_rate:.2%}")
                    st.write(f"Prone Hit Rate: {prone_hit_rate:.2%}")
                    st.write(f"Standing Hit Rate: {standing_hit_rate:.2%}")
                else:
                    st.write("No hit rate data available.")
            with col4:
                if overall_hit_rate is not None:
                    st.markdown(f"<div style='width: 30px; height: 30px; background-color: {get_color_for_hit_rate(overall_hit_rate)}'></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='width: 30px; height: 30px; background-color: {get_color_for_hit_rate(prone_hit_rate)}'></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='width: 30px; height: 30px; background-color: {get_color_for_hit_rate(standing_hit_rate)}'></div>", unsafe_allow_html=True)
                else:
                    st.write("")
            st.markdown("---")  # Trennlinie zwischen den Athleten
    else:
        st.write("No athletes in your team yet.")

def show_stats():
    if 'trainer_team' in st.session_state and st.session_state.trainer_team:
        athlete_names = [f"{athlete['first_name']} {athlete['last_name']}" for athlete in st.session_state.trainer_team]
        
        # Berechnung der durchschnittlichen Trefferquote des gesamten Teams
        total_hit_rate = 0
        total_prone_hit_rate = 0
        total_standing_hit_rate = 0
        total_athletes = 0

        for athlete in st.session_state.trainer_team:
            statistics_file = f"JSON/biathlon_statistics_K_{athlete['first_name']}_{athlete['last_name']}.json"
            try:
                with open(statistics_file, 'r') as file:
                    statistics = json.load(file)
                total_shots = af.calculate_total_shots(statistics)
                total_prone_errors = af.calculate_prone_errors(statistics)
                total_standing_errors = af.calculate_standing_errors(statistics)
                overall_hit_rate, prone_hit_rate, standing_hit_rate = af.calculate_hit_rate(total_shots, total_prone_errors, total_standing_errors)
                total_hit_rate += overall_hit_rate
                total_prone_hit_rate += prone_hit_rate
                total_standing_hit_rate += standing_hit_rate
                total_athletes += 1
            except FileNotFoundError:
                continue

        if total_athletes > 0:
            avg_team_hit_rate = (total_hit_rate / total_athletes) * 100
            avg_team_prone_hit_rate = (total_prone_hit_rate / total_athletes) * 100
            avg_team_standing_hit_rate = (total_standing_hit_rate / total_athletes) * 100
        else:
            avg_team_hit_rate = 0
            avg_team_prone_hit_rate = 0
            avg_team_standing_hit_rate = 0

        # Anzeigen der Teamstatistiken
        st.subheader("Team Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Mean Team Hitrate: {avg_team_hit_rate:.2f}%")
            
        with col2:
            st.write(f"Mean Team Hitrate Prone: {avg_team_prone_hit_rate:.2f}%")
            st.write(f"Mean Team Hitrate Standing: {avg_team_standing_hit_rate:.2f}%")
        
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

    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

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

if __name__ == "__main__":
    trainer_app()