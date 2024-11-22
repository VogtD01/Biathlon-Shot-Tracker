import analyse_functions as af
import streamlit as st
import os
from datetime import datetime

# Den jetzigen Benutzer auslesen oder initialisieren
if 'user' not in st.session_state:
    st.session_state['user'] = {'first_name': 'Default', 'last_name': 'User'}  # Beispielwerte, anpassen wie nötig

user = st.session_state['user']


def plot_user_hit_rate_over_time(user, mode=None, training_mode=None):
    # Datei Pfad basierend auf dem Benutzer
    file_path = os.path.join("JSON", f"biathlon_statistics_K_{user['first_name']}_{user['last_name']}.json")

    # Eingabefelder für Start- und Enddatum nebeneinander
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime(2021, 1, 1)).strftime("%Y-%m-%d")
    with col2:
        end_date = st.date_input("End Date", value=datetime.now()).strftime("%Y-%m-%d")

    # Trefferquoten über die Zeit sammeln
    hit_rates_over_time, hit_rate_prone_over_time, hit_rate_standing_over_time, discipline_name = af.collect_hit_rates(file_path, mode=mode, training_mode=training_mode)

    # Daten nach dem angegebenen Zeitraum filtern
    hit_rates_over_time = [(date, rate) for date, rate in hit_rates_over_time if start_date <= date <= end_date]
    hit_rate_prone_over_time = [(date, rate) for date, rate in hit_rate_prone_over_time if start_date <= date <= end_date]
    hit_rate_standing_over_time = [(date, rate) for date, rate in hit_rate_standing_over_time if start_date <= date <= end_date]

    # Checkbox für das Anzeigen der Prone/Standing Trefferquoten
    show_prone_standing = st.checkbox("Show Prone/Standing Hit Rate", value=True)

    # Trefferquoten über die Zeit ausplotten
    af.plot_hit_rates(hit_rates_over_time, hit_rate_prone_over_time, hit_rate_standing_over_time, show_prone_standing)
    
     # Durchschnittswerte berechnen
    avg_hit_rate = calculate_average(hit_rates_over_time) *100
    avg_prone_hit_rate = calculate_average(hit_rate_prone_over_time) *100
    avg_standing_hit_rate = calculate_average(hit_rate_standing_over_time) *100

   # Display average values if they are not 0
    if avg_hit_rate != 0:
        st.write(f"Average Hit Rate: {avg_hit_rate:.2f}%")
    if avg_prone_hit_rate != 0:
        st.write(f"Average Prone Hit Rate: {avg_prone_hit_rate:.2f}%")
    if avg_standing_hit_rate != 0:
        st.write(f"Average Standing Hit Rate: {avg_standing_hit_rate:.2f}%")
    
    af.plot_smoothed_hit_rates(hit_rates_over_time, hit_rate_prone_over_time, hit_rate_standing_over_time, show_prone_standing)

def plot_discipline_hit_rate(user, discipline_name, mode=None, training_mode=None):
    # Datei Pfad basierend auf dem Benutzer
    file_path = os.path.join("JSON", f"biathlon_statistics_K_{user['first_name']}_{user['last_name']}.json")

    # Eingabefelder für Start- und Enddatum nebeneinander
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime(2021, 1, 1), key=f"start_date_{discipline_name}").strftime("%Y-%m-%d")
    with col2:
        end_date = st.date_input("End Date", value=datetime.now(), key=f"end_date_{discipline_name}").strftime("%Y-%m-%d")

    # Trefferquoten über die Zeit sammeln für die gewählte Disziplin
    hit_rates_over_time, hit_rate_prone_over_time, hit_rate_standing_over_time, _ = af.collect_hit_rates(file_path, discipline_name, mode=mode, training_mode=training_mode)

    # Daten nach dem angegebenen Zeitraum filtern
    hit_rates_over_time = [(date, rate) for date, rate in hit_rates_over_time if start_date <= date <= end_date]
    hit_rate_prone_over_time = [(date, rate) for date, rate in hit_rate_prone_over_time if start_date <= date <= end_date]
    hit_rate_standing_over_time = [(date, rate) for date, rate in hit_rate_standing_over_time if start_date <= date <= end_date]

    # Checkbox für das Anzeigen der Prone/Standing Trefferquoten
    show_prone_standing = st.checkbox(f"Show Prone/Standing Hit Rate for {discipline_name}", value=True, key=f"checkbox_{discipline_name}")

    # Trefferquoten über die Zeit ausplotten
    af.plot_hit_rates(hit_rates_over_time, hit_rate_prone_over_time, hit_rate_standing_over_time, show_prone_standing, discipline_name)
    
     # Durchschnittswerte berechnen
    avg_hit_rate = calculate_average(hit_rates_over_time) *100
    avg_prone_hit_rate = calculate_average(hit_rate_prone_over_time) *100
    avg_standing_hit_rate = calculate_average(hit_rate_standing_over_time) *100

    
    # Display average values if they are not 0
    if avg_hit_rate != 0:
        st.write(f"Average Hit Rate: {avg_hit_rate:.2f}%")
    if avg_prone_hit_rate != 0:
        st.write(f"Average Prone Hit Rate: {avg_prone_hit_rate:.2f}%")
    if avg_standing_hit_rate != 0:
        st.write(f"Average Standing Hit Rate: {avg_standing_hit_rate:.2f}%")
    # Trefferquoten smooth ausplotten
    af.plot_smoothed_hit_rates(hit_rates_over_time, hit_rate_prone_over_time, hit_rate_standing_over_time, show_prone_standing, discipline_name)
    
def plot_discipline_comparison(user, mode=None, training_mode=None):
    # Datei Pfad basierend auf dem Benutzer
    file_path = os.path.join("JSON", f"biathlon_statistics_K_{user['first_name']}_{user['last_name']}.json")

    # Disziplinen vergleichen
    discipline_stats = af.compare_disciplines(file_path, mode=mode, training_mode=training_mode)
    af.plot_discipline_comparison(discipline_stats)

def plot_wind_condition_comparison(user, mode=None, training_mode=None):
    # Datei Pfad basierend auf dem Benutzer
    file_path = os.path.join("JSON", f"biathlon_statistics_K_{user['first_name']}_{user['last_name']}.json")

    # Windbedingungen vergleichen
    wind_stats = af.compare_wind_conditions(file_path, mode=mode, training_mode=training_mode)
    af.plot_wind_condition_comparison(wind_stats)

def calculate_average(hit_rates):
        return sum(rate for _, rate in hit_rates) / len(hit_rates) if hit_rates else 0


# Hauptfunktion
def main(user):
    st.title(f"Hit Rate Analysis for {user['first_name']} {user['last_name']}")

    # Auswahl des Modus
    mode_option = st.selectbox("Select Mode", ["All", "Training", "Competition"])
    mode = None if mode_option == "All" else mode_option

    training_mode = None
    if mode == "Training":
        training_mode = st.selectbox("Select Training Mode", ["All", "TNS", "Komplex"])
        training_mode = None if training_mode == "All" else training_mode

    # Auswahl der Analyseoption
    analysis_option = st.selectbox("Select Analysis Option", ["Overall Hit Rate", "Discipline Hit Rate", "Discipline Comparison", "Wind Condition Comparison"])

    if analysis_option == "Overall Hit Rate":
        plot_user_hit_rate_over_time(user, mode, training_mode)
    elif analysis_option == "Discipline Hit Rate":
        cols = st.columns(4)
        with cols[0]:
            sprint_selected = st.checkbox("Sprint")
        with cols[1]:
            individual_selected = st.checkbox("Individual")
        with cols[2]:
            mass_start_selected = st.checkbox("Mass Start")
        with cols[3]:
            pursuit_selected = st.checkbox("Pursuit")

        if sprint_selected:
            plot_discipline_hit_rate(user, "Sprint", mode, training_mode)
        if individual_selected:
            plot_discipline_hit_rate(user, "Individual", mode, training_mode)
        if mass_start_selected:
            plot_discipline_hit_rate(user, "Mass Start", mode, training_mode)
        if pursuit_selected:
            plot_discipline_hit_rate(user, "Pursuit", mode, training_mode)
    elif analysis_option == "Discipline Comparison":
        plot_discipline_comparison(user, mode, training_mode)
    elif analysis_option == "Wind Condition Comparison":
        plot_wind_condition_comparison(user, mode, training_mode)

if __name__ == "__main__":
    main(user)

    ##########################test