import streamlit as st
import json

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
    st.title("Trainer App")

    # Check if the logged-in user is Trainer Huber
    if st.session_state.user['first_name'].lower() == 'trainer' and st.session_state.user['last_name'].lower() == 'huber':
        st.subheader("Welcome, Trainer Huber!")

        trainer_name = f"{st.session_state.user['first_name'].lower()}_{st.session_state.user['last_name'].lower()}"

        # Load the trainer's team from the JSON file
        if 'trainer_team' not in st.session_state:
            st.session_state.trainer_team = load_trainer_team(trainer_name)

        # Page navigation
        page = st.sidebar.selectbox("Select Page", ["Your Team", "Stats", "Team Management"])

        if page == "Your Team":
            show_team()
        elif page == "Stats":
            show_stats()
        elif page == "Team Management":
            team_management(trainer_name)
    else:
        st.error("You are not authorized to access this page.")

def show_team():
    st.subheader("Your Team")
    if 'trainer_team' in st.session_state and st.session_state.trainer_team:
        for athlete in st.session_state.trainer_team:
            st.write(f"{athlete['first_name']} {athlete['last_name']}")
    else:
        st.write("No athletes in your team yet.")

def show_stats():
    st.subheader("Stats")
    st.write("Stats page is under construction.")

def team_management(trainer_name):
    st.subheader("Team Management")

    # Load all athletes
    athletes = load_athletes()

    # Select athletes for the trainer's team
    st.subheader("Select Athletes for Your Team")
    selected_athletes = st.multiselect(
        "Select Athletes",
        options=[f"{athlete['first_name']} {athlete['last_name']}" for athlete in athletes]
    )

    # Save the selected athletes to the trainer's team
    if st.button("Save Team"):
        trainer_team = [athlete for athlete in athletes if f"{athlete['first_name']} {athlete['last_name']}" in selected_athletes]
        st.session_state.trainer_team = trainer_team
        save_trainer_team(trainer_team, trainer_name)
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
#     {"first_name": "John", "last_name": "Doe"},
#     {"first_name": "Jane", "last_name": "Smith"},
#     {"first_name": "Emily", "last_name": "Jones"},
#     {"first_name": "Trainer", "last_name": "Huber"}
# ]

# Example trainer_huber_team.json content:
# [
#     {"first_name": "John", "last_name": "Doe"},
#     {"first_name": "Jane", "last_name": "Smith"}
# ]

if __name__ == "__main__":
    trainer_app()