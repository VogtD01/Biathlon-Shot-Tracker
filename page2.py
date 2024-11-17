import json
import os
import streamlit as st
import matplotlib.pyplot as plt
from collections import defaultdict


def load_statistics(file_path):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, "r") as file:
            try:
                statistics = json.load(file)
                return statistics
            except json.JSONDecodeError:
                st.error("Error decoding JSON file.")
                return None
    else:
        st.error("File does not exist or is empty.")
        return None

def calculate_total_shots(statistics):
    total_shots = 0
    for entry in statistics:
        if "Daily Summary" in entry and "Total Shots" in entry["Daily Summary"]:
            total_shots += entry["Daily Summary"]["Total Shots"]
    return total_shots

def calculate_prone_errors(statistics):
    total_prone_errors = 0
    for entry in statistics:
        if "Daily Summary" in entry and "Prone Errors" in entry["Daily Summary"]:
            total_prone_errors += entry["Daily Summary"]["Prone Errors"]
    return total_prone_errors

def calculate_standing_errors(statistics):
    total_standing_errors = 0
    for entry in statistics:
        if "Daily Summary" in entry and "Standing Errors" in entry["Daily Summary"]:
            total_standing_errors += entry["Daily Summary"]["Standing Errors"]
    return total_standing_errors

def calculate_hit_rate(total_shots, total_prone_errors, total_standing_errors):
    overall_hit_rate = 1 - (total_prone_errors + total_standing_errors) / total_shots
    prone_hit_rate = 1 - total_prone_errors / (total_shots/2)
    standing_hit_rate = 1 - total_standing_errors / (total_shots/2)
    return overall_hit_rate, prone_hit_rate, standing_hit_rate




def analyze_discipline_old(file_path, discipline_name, mode=None, training_mode=None):
    statistics = load_statistics(file_path)
    if not statistics:
        return None, None, None, None, None, None, None

    discipline_count = 0
    total_shots = 0
    total_prone_errors = 0
    total_standing_errors = 0

    # Setze die Anzahl der Schüsse pro Instanz basierend auf der Disziplin
    shots_per_instance = 10 if discipline_name == "Sprint" else 20

    for entry in statistics:
        if "Discipline Details" in entry:
            for discipline in entry["Discipline Details"]:
                if discipline["Discipline"] == discipline_name:
                    if (mode is None or entry["Mode"] == mode) and (training_mode is None or entry["Trainings_mode"] == training_mode):
                        discipline_count += 1
                        total_shots += shots_per_instance
                        total_prone_errors += discipline["Errors"]["Prone"]
                        total_standing_errors += discipline["Errors"]["Standing"]

    if total_shots > 0:
        hit_rate = 1 - (total_prone_errors + total_standing_errors) / total_shots
        hit_rate_prone = 1 - total_prone_errors / (total_shots / 2)
        hit_rate_standing = 1 - total_standing_errors / (total_shots / 2)
    else:
        hit_rate = hit_rate_prone = hit_rate_standing = 0

    return discipline_count, total_shots, total_prone_errors, total_standing_errors, hit_rate, hit_rate_prone, hit_rate_standing

def analyze_discipline(file_path, discipline_name, mode=None, training_mode=None, wind_condition=None):
    statistics = load_statistics(file_path)
    if not statistics:
        return None, None, None, None, None, None, None

    discipline_count = 0
    total_shots = 0
    total_prone_errors = 0
    total_standing_errors = 0

    # Setze die Anzahl der Schüsse pro Instanz basierend auf der Disziplin
    shots_per_instance = 10 if discipline_name == "Sprint" else 20

    for entry in statistics:
        if "Discipline Details" in entry:
            for discipline in entry["Discipline Details"]:
                if discipline["Discipline"] == discipline_name:
                    if (mode is None or entry["Mode"] == mode) and (training_mode is None or entry["Trainings_mode"] == training_mode) and (wind_condition is None or entry["Wind Conditions"] == wind_condition):
                        discipline_count += 1
                        total_shots += shots_per_instance
                        total_prone_errors += discipline["Errors"]["Prone"]
                        total_standing_errors += discipline["Errors"]["Standing"]

    if total_shots > 0:
        hit_rate = 1 - (total_prone_errors + total_standing_errors) / total_shots
        hit_rate_prone = 1 - total_prone_errors / (total_shots / 2)
        hit_rate_standing = 1 - total_standing_errors / (total_shots / 2)
    else:
        hit_rate = hit_rate_prone = hit_rate_standing = 0

    return discipline_count, total_shots, total_prone_errors, total_standing_errors, hit_rate, hit_rate_prone, hit_rate_standing

def collect_overall_hit_rates(file_path):
    statistics = load_statistics(file_path)
    if not statistics:
        return [], [], []

    overall_hit_rates_over_time = []
    prone_hit_rates_over_time = []
    standing_hit_rates_over_time = []

    for entry in statistics:
        date = entry["Date"]
        overall_hit_rate = entry["Daily Summary"]["Overall Hit Rate"]
        prone_hit_rate = entry["Daily Summary"]["Prone Hit Rate"]
        standing_hit_rate = entry["Daily Summary"]["Standing Hit Rate"]

        overall_hit_rates_over_time.append((date, overall_hit_rate))
        prone_hit_rates_over_time.append((date, prone_hit_rate))
        standing_hit_rates_over_time.append((date, standing_hit_rate))

    return overall_hit_rates_over_time, prone_hit_rates_over_time, standing_hit_rates_over_time

def collect_hit_rates(file_path, discipline_name, mode=None, training_mode=None):
    statistics = load_statistics(file_path)
    if not statistics:
        return [], [], []

    hit_rates_over_time = defaultdict(list)
    hit_rate_prone_over_time = defaultdict(list)
    hit_rate_standing_over_time = defaultdict(list)

    # Setze die Anzahl der Schüsse pro Instanz basierend auf der Disziplin
    shots_per_instance = 10 if discipline_name == "Sprint" else 20

    for entry in statistics:
        if "Discipline Details" in entry:
            for discipline in entry["Discipline Details"]:
                if discipline["Discipline"] == discipline_name:
                    if (mode is None or entry["Mode"] == mode) and (training_mode is None or entry["Trainings_mode"] == training_mode):
                        total_shots = shots_per_instance
                        total_prone_errors = discipline["Errors"]["Prone"]
                        total_standing_errors = discipline["Errors"]["Standing"]

                        if total_shots > 0:
                            hit_rate = 1 - (total_prone_errors + total_standing_errors) / total_shots
                            hit_rate_prone = 1 - total_prone_errors / (total_shots / 2)
                            hit_rate_standing = 1 - total_standing_errors / (total_shots / 2)
                        else:
                            hit_rate = hit_rate_prone = hit_rate_standing = 0

                        hit_rates_over_time[entry["Date"]].append(hit_rate)
                        hit_rate_prone_over_time[entry["Date"]].append(hit_rate_prone)
                        hit_rate_standing_over_time[entry["Date"]].append(hit_rate_standing)

    # Durchschnitt der Trefferquoten für jedes Datum berechnen
    avg_hit_rates_over_time = [(date, sum(rates) / len(rates)) for date, rates in hit_rates_over_time.items()]
    avg_hit_rate_prone_over_time = [(date, sum(rates) / len(rates)) for date, rates in hit_rate_prone_over_time.items()]
    avg_hit_rate_standing_over_time = [(date, sum(rates) / len(rates)) for date, rates in hit_rate_standing_over_time.items()]

    return avg_hit_rates_over_time, avg_hit_rate_prone_over_time, avg_hit_rate_standing_over_time

def compare_disciplines(file_path):
    disciplines = ["Individual", "Mass Start", "Sprint", "Pursuit"]
    discipline_stats = {}

    for discipline in disciplines:
        count, total_shots, total_prone_errors, total_standing_errors, hit_rate, hit_rate_prone, hit_rate_standing = analyze_discipline(file_path, discipline)
        discipline_stats[discipline] = {
            "count": count,
            "total_shots": total_shots,
            "total_prone_errors": total_prone_errors,
            "total_standing_errors": total_standing_errors,
            "hit_rate": hit_rate,
            "hit_rate_prone": hit_rate_prone,
            "hit_rate_standing": hit_rate_standing
        }

    return discipline_stats

def compare_wind_conditions(file_path):

    wind_conditions = ["Calm", "Light Wind", "Windy", "Stormy"]
    wind_stats = {condition: {"total_shots": 0, "total_prone_errors": 0, "total_standing_errors": 0, "hit_rate": 0} for condition in wind_conditions}

    statistics = load_statistics(file_path)
    if not statistics:
        return wind_stats

    for entry in statistics:
        condition = entry["Wind Conditions"]
        if condition in wind_conditions:
            for discipline in entry["Discipline Details"]:
                shots_per_instance = 10 if discipline["Discipline"] == "Sprint" else 20
                wind_stats[condition]["total_shots"] += shots_per_instance
                wind_stats[condition]["total_prone_errors"] += discipline["Errors"]["Prone"]
                wind_stats[condition]["total_standing_errors"] += discipline["Errors"]["Standing"]

    for condition in wind_conditions:
        total_shots = wind_stats[condition]["total_shots"]
        total_errors = wind_stats[condition]["total_prone_errors"] + wind_stats[condition]["total_standing_errors"]
        if total_shots > 0:
            wind_stats[condition]["hit_rate"] = 1 - total_errors / total_shots
        else:
            wind_stats[condition]["hit_rate"] = 0

    return wind_stats

def plot_overall_hit_rates(overall_hit_rates_over_time, prone_hit_rates_over_time=None, standing_hit_rates_over_time=None, show_prone_standing=False):
    if not overall_hit_rates_over_time and not (show_prone_standing and prone_hit_rates_over_time) and not (show_prone_standing and standing_hit_rates_over_time):
        st.write("No data available to plot.")
        return

    fig, ax = plt.subplots(figsize=(10, 5))

    has_data = False

    if overall_hit_rates_over_time:
        dates, overall_hit_rates = zip(*overall_hit_rates_over_time)
        ax.plot(dates, overall_hit_rates, marker='o', linestyle='-', color='b', label='Overall Hit Rate')
        has_data = True

    if show_prone_standing and prone_hit_rates_over_time:
        dates_prone, prone_hit_rates = zip(*prone_hit_rates_over_time)
        ax.plot(dates_prone, prone_hit_rates, marker='o', linestyle='--', color='gray', label='Prone Hit Rate')
        has_data = True

    if show_prone_standing and standing_hit_rates_over_time:
        dates_standing, standing_hit_rates = zip(*standing_hit_rates_over_time)
        ax.plot(dates_standing, standing_hit_rates, marker='o', linestyle='-.', color='gray', label='Standing Hit Rate')
        has_data = True

    ax.set_xlabel('Date')
    ax.set_ylabel('Hit Rate')
    ax.set_title('Hit Rate Over Time')
    ax.tick_params(axis='x', rotation=45)
    
    # Nur die Legende anzeigen, wenn es Daten gibt
    if has_data:
        ax.legend()

    ax.grid(True)
    plt.tight_layout()

    st.pyplot(fig)

def plot_hit_rates(hit_rates_over_time, hit_rate_prone_over_time=None, hit_rate_standing_over_time=None, show_prone_standing=False):
    if not hit_rates_over_time and not (show_prone_standing and hit_rate_prone_over_time) and not (show_prone_standing and hit_rate_standing_over_time):
        st.write("No data available to plot.")
        return

    plt.figure(figsize=(10, 5))

    has_data = False

    if hit_rates_over_time:
        dates, hit_rates = zip(*hit_rates_over_time)
        plt.plot(dates, hit_rates, marker='o', linestyle='-', color='b', label='Total Hit Rate')
        has_data = True

    if show_prone_standing and hit_rate_prone_over_time:
        dates_prone, hit_rates_prone = zip(*hit_rate_prone_over_time)
        plt.plot(dates_prone, hit_rates_prone, marker='o', linestyle='--', color='gray', label='Prone Hit Rate')
        has_data = True

    if show_prone_standing and hit_rate_standing_over_time:
        dates_standing, hit_rates_standing = zip(*hit_rate_standing_over_time)
        plt.plot(dates_standing, hit_rates_standing, marker='o', linestyle='-.', color='gray', label='Standing Hit Rate')
        has_data = True

    plt.xlabel('Date')
    plt.ylabel('Hit Rate')
    plt.title('Hit Rate Over Time')
    plt.xticks(rotation=45)
    
    # Nur die Legende anzeigen, wenn es Daten gibt
    if has_data:
        plt.legend()

    plt.grid(True)
    plt.tight_layout()

    st.pyplot(plt)

def plot_discipline_comparison(discipline_stats):
    if not discipline_stats:
        st.write("No data available to plot.")
        return

    disciplines = list(discipline_stats.keys())
    hit_rates = [discipline_stats[discipline]["hit_rate"] for discipline in disciplines]

    plt.figure(figsize=(10, 5))
    plt.bar(disciplines, hit_rates, color=['blue', 'green', 'red', 'purple'])
    plt.xlabel('Discipline')
    plt.ylabel('Hit Rate')
    plt.title('Hit Rate Comparison Across Disciplines')
    plt.ylim(0, 1)
    plt.grid(True)
    plt.tight_layout()

    st.pyplot(plt)

def plot_wind_condition_comparison(wind_stats):
    if not wind_stats:
        st.write("No data available to plot.")
        return

    conditions = list(wind_stats.keys())
    hit_rates = [wind_stats[condition]["hit_rate"] for condition in conditions]

    plt.figure(figsize=(10, 5))
    plt.bar(conditions, hit_rates, color=['blue', 'green', 'red', 'purple'])
    plt.xlabel('Wind Conditions')
    plt.ylabel('Hit Rate')
    plt.title('Hit Rate Comparison Across Wind Conditions')
    plt.ylim(0, 1)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)

#######################################################################################
def main():
    st.title("Biathlon Statistics")

    file_path = os.path.join("JSON", "biathlon_statistics_K_DV_01.json")
    statistics = load_statistics(file_path)

    if statistics:
        total_shots = calculate_total_shots(statistics)
        total_prone_errors = calculate_prone_errors(statistics)
        total_standing_errors = calculate_standing_errors(statistics)

        #Sprint statistics
        #sprint_count, total_shots_sprint, total_prone_errors_sprint, total_standing_errors_sprint, sprint_hit_rate, sprint_hit_rate_prone, sprint_hit_rate_standing = analyze_discipline(file_path, "Sprint")

        #individual statistics
        #individual_count, total_shots_individual, total_prone_errors_individual, total_standing_errors_individual, individual_hit_rate, individual_hit_rate_prone, individual_hit_rate_standing = analyze_discipline(file_path, "Individual")

       
        # Individual statistics all
        #ind_all_c, ts_all_c, pe_all_c, se_all_c, hr_all_c, hrp_all_c, hrs_all_c = analyze_discipline(file_path, "Individual")

        # Individual statistics training
        #ind_tr_c, ts_tr_c, pe_tr_c, se_tr_c, hr_tr_c, hrp_tr_c, hrs_tr_c = analyze_discipline(file_path, "Individual", mode="Training")

        # Individual statistics competition
        #ind_comp_c, ts_comp_c, pe_comp_c, se_comp_c, hr_comp_c, hrp_comp_c, hrs_comp_c = analyze_discipline(file_path, "Individual", mode="Competition")

        # Show individual statistics all, komplex
       # ind_all_k_c, ts_all_k_c, pe_all_k_c, se_all_k_c, hr_all_k_c, hrp_all_k_c, hrs_all_k_c = analyze_discipline(file_path, "Individual", training_mode="Komplex")

        # Show individual statistics training, komplex 
        #ind_tr_k_c, ts_tr_k_c, pe_tr_k_c, se_tr_k_c, hr_tr_k_c, hrp_tr_k_c, hrs_tr_k_c = analyze_discipline(file_path, "Individual", mode="Training", training_mode="Komplex")

        # Show individual statistics training, TNS
        #ind_tr_tns_c, ts_tr_tns_c, pe_tr_tns_c, se_tr_tns_c, hr_tr_tns_c, hrp_tr_tns_c, hrs_tr_tns_c = analyze_discipline(file_path, "Individual", training_mode="TNS")
        #---------------------------------------
        
        hit_rates_over_time, hit_rate_prone_over_time, hit_rate_standing_over_time = collect_hit_rates(file_path, "Individual")

        show_prone_standing = st.checkbox("Show Prone/Standing Hit Rate", value=True)


        plot_hit_rates(hit_rates_over_time, hit_rate_prone_over_time, hit_rate_standing_over_time, show_prone_standing)

        # Compare disciplines
        discipline_stats = compare_disciplines(file_path)
        plot_discipline_comparison(discipline_stats)

        # Compare wind conditions globally across all disciplines
        wind_stats = compare_wind_conditions(file_path)
        
        plot_wind_condition_comparison(wind_stats)

        #---------------------------------
        #analyse individual
        ind_all_c, ts_all_c, pe_all_c, se_all_c, hr_all_c, hrp_all_c, hrs_all_c = analyze_discipline(file_path, "Individual")
        st.write("Individual statistics all")
        st.write(f"Count: {ind_all_c}")
        st.write(f"Total Shots: {ts_all_c}")

        hit_rates_over_time, hit_rate_prone_over_time, hit_rate_standing_over_time = collect_hit_rates(file_path, "Individual")
        st.write("hir rates over time")
        #st.write(hit_rates_over_time, hit_rate_prone_over_time, hit_rate_standing_over_time)

        #
        overall_hit_rates_over_time, prone_hit_rates_over_time, standing_hit_rates_over_time = collect_overall_hit_rates(file_path)
        show_prone_standing = st.checkbox("Show Prone/Standing Hit Rate2", value=True)
        plot_overall_hit_rates(overall_hit_rates_over_time, prone_hit_rates_over_time, standing_hit_rates_over_time, show_prone_standing)


        


main()

    