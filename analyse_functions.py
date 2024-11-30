import json
import os
import streamlit as st
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.interpolate import make_interp_spline
import numpy as np

#---Calculate Functions--------------------------------------------------------------------------------------------------------------
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

#---Analyse Functions--------------------------------------------------------------

def analyze_discipline(file_path, discipline_name=None, mode=None, training_mode=None, wind_condition=None):
    statistics = load_statistics(file_path)
    if not statistics:
        return None, None, None, None, None, None, None

    discipline_count = 0
    total_shots = 0
    total_prone_errors = 0
    total_standing_errors = 0

    for entry in statistics:
        if "Discipline Details" in entry:
            for discipline in entry["Discipline Details"]:
                if (discipline_name is None or discipline["Discipline"] == discipline_name):
                    if (mode is None or entry["Mode"] == mode) and (training_mode is None or entry["Trainings_mode"] == training_mode) and (wind_condition is None or entry["Wind Conditions"] == wind_condition):
                        shots_per_instance = 10 if discipline["Discipline"] == "Sprint" else 20
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

def collect_hit_rates(file_path, discipline_name=None, mode=None, training_mode=None):
    statistics = load_statistics(file_path)
    if not statistics:
        return [], [], [], discipline_name

    hit_rates_over_time = defaultdict(list)
    hit_rate_prone_over_time = defaultdict(list)
    hit_rate_standing_over_time = defaultdict(list)

    for entry in statistics:
        if "Discipline Details" in entry:
            for discipline in entry["Discipline Details"]:
                if (discipline_name is None or discipline["Discipline"] == discipline_name):
                    if (mode is None or entry["Mode"] == mode) and (training_mode is None or entry["Trainings_mode"] == training_mode):
                        shots_per_instance = 10 if discipline["Discipline"] == "Sprint" else 20
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

    return avg_hit_rates_over_time, avg_hit_rate_prone_over_time, avg_hit_rate_standing_over_time, discipline_name

def compare_disciplines(file_path, mode=None, training_mode=None):
    disciplines = ["Individual", "Mass Start", "Sprint", "Pursuit"]
    discipline_stats = {}

    for discipline in disciplines:
        count, total_shots, total_prone_errors, total_standing_errors, hit_rate, hit_rate_prone, hit_rate_standing = analyze_discipline(file_path, discipline, mode=mode, training_mode=training_mode)
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

def compare_wind_conditions(file_path, mode=None, training_mode=None):
    wind_conditions = ["Calm", "Light Wind", "Windy", "Stormy"]
    wind_stats = {condition: {"total_shots": 0, "total_prone_errors": 0, "total_standing_errors": 0, "hit_rate": 0} for condition in wind_conditions}

    statistics = load_statistics(file_path)
    if not statistics:
        return wind_stats

    for entry in statistics:
        if (mode is None or entry["Mode"] == mode) and (training_mode is None or entry["Trainings_mode"] == training_mode):
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


#--- Plot Functions--------------------------------------------------------------------------------------------------------------
sns.set_theme(style="darkgrid")  # Stil für dunkles Design mit Gitter

def plot_overall_hit_rates(overall_hit_rates_over_time, prone_hit_rates_over_time=None, standing_hit_rates_over_time=None, show_prone_standing=False):
    if not overall_hit_rates_over_time and not (show_prone_standing and prone_hit_rates_over_time) and not (show_prone_standing and standing_hit_rates_over_time):
        st.write("No data available to plot.")
        return

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('black')  # Hintergrund des gesamten Plots
    ax.set_facecolor('black')  # Hintergrund der Achsen

    if overall_hit_rates_over_time:
        dates, overall_hit_rates = zip(*overall_hit_rates_over_time)
        ax.plot(dates, overall_hit_rates, marker='o', linestyle='-', color='#00FFFF', label='Overall Hit Rate', linewidth=2)  # Cyan

    if show_prone_standing and prone_hit_rates_over_time:
        dates_prone, prone_hit_rates = zip(*prone_hit_rates_over_time)
        ax.plot(dates_prone, prone_hit_rates, marker='s', linestyle='--', color='#FF4500', label='Prone Hit Rate', linewidth=1.5)  # Orange-rot

    if show_prone_standing and standing_hit_rates_over_time:
        dates_standing, standing_hit_rates = zip(*standing_hit_rates_over_time)
        ax.plot(dates_standing, standing_hit_rates, marker='d', linestyle='-.', color='#32CD32', label='Standing Hit Rate', linewidth=1.5)  # Leuchtend Grün

    ax.set_title('Hit Rate Over Time', fontsize=18, color='white', weight='bold', pad=20)
    ax.set_xlabel('Date', fontsize=14, color='white', labelpad=10)
    ax.set_ylabel('Hit Rate (%)', fontsize=14, color='white', labelpad=10)
    ax.tick_params(axis='x', rotation=45, labelsize=12, colors='white')
    ax.tick_params(axis='y', labelsize=12, colors='white')
    ax.legend(loc='upper left', fontsize=12, frameon=False, facecolor='black', edgecolor='black', labelcolor='white')
    ax.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.7, color='gray')

    fig.tight_layout()
    st.pyplot(fig)

def plot_hit_rates(hit_rates_over_time, hit_rate_prone_over_time=None, hit_rate_standing_over_time=None, show_prone_standing=False, discipline_name=None):
    if not hit_rates_over_time and not (show_prone_standing and hit_rate_prone_over_time) and not (show_prone_standing and hit_rate_standing_over_time):
        st.write("No data available to plot.")
        return

    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor('black')  # Hintergrund des gesamten Plots
    ax.set_facecolor('black')  # Hintergrund der Achsen

    has_data = False

    if hit_rates_over_time:
        dates, hit_rates = zip(*hit_rates_over_time)
        ax.plot(dates, hit_rates, marker='o', linestyle='-', color='#00FFFF', label='Total Hit Rate')  # Cyan
        has_data = True

    if show_prone_standing and hit_rate_prone_over_time:
        dates_prone, hit_rates_prone = zip(*hit_rate_prone_over_time)
        ax.plot(dates_prone, hit_rates_prone, marker='o', linestyle='-', color='#FF4500', label='Prone Hit Rate')  # Orange-rot
        has_data = True

    if show_prone_standing and hit_rate_standing_over_time:
        dates_standing, hit_rates_standing = zip(*hit_rate_standing_over_time)
        ax.plot(dates_standing, hit_rates_standing, marker='o', linestyle='-', color='#32CD32', label='Standing Hit Rate')  # Leuchtend Grün
        has_data = True

    ax.set_xlabel('Date', fontsize=14, color='white', labelpad=10)
    ax.set_ylabel('Hit Rate (%)', fontsize=14, color='white', labelpad=10)
    title = 'Hit Rate Over Time'
    if discipline_name:
        title += f' for {discipline_name}'
    ax.set_title(title, fontsize=18, color='white', weight='bold', pad=20)
    ax.tick_params(axis='x', rotation=45, labelsize=12, colors='white')
    ax.tick_params(axis='y', labelsize=12, colors='white')

    if has_data:
        ax.legend(loc='upper left', fontsize=12, frameon=False, facecolor='black', edgecolor='black', labelcolor='white')

    ax.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.7, color='gray')

    fig.tight_layout()
    st.pyplot(fig)

def smooth_data(data):
    smoothed_data = []
    for i in range(len(data)):
        if i == 0:
            # Kein vorheriger Wert
            smoothed_data.append(data[i])
        elif i == len(data) - 1:
            # Kein nächster Wert
            smoothed_data.append(data[i])
        else:
            # Durchschnitt aus vorherigem, aktuellem und nächstem Wert
            smoothed_value = (data[i-1] + data[i] + data[i+1]) / 3
            smoothed_data.append(smoothed_value)
    return smoothed_data

def plot_smoothed_hit_rates(hit_rates_over_time, hit_rate_prone_over_time=None, hit_rate_standing_over_time=None, show_prone_standing=False, discipline_name=None):
    if not hit_rates_over_time and not (show_prone_standing and hit_rate_prone_over_time) and not (show_prone_standing and hit_rate_standing_over_time):
        st.write("No data available to plot.")
        return

    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor('black')  # Hintergrund des gesamten Plots
    ax.set_facecolor('black')  # Hintergrund der Achsen

    has_data = False

    if hit_rates_over_time:
        dates, hit_rates = zip(*hit_rates_over_time)
        smoothed_hit_rates = smooth_data(hit_rates)
        dates_num = np.arange(len(dates))
        hit_rates_smooth = make_interp_spline(dates_num, smoothed_hit_rates, k=2)(dates_num)
        ax.plot(dates, hit_rates_smooth, marker='', linestyle='-', color='#00FFFF', label='Total Hit Rate')  # Cyan
        has_data = True

    if show_prone_standing and hit_rate_prone_over_time:
        dates_prone, hit_rates_prone = zip(*hit_rate_prone_over_time)
        smoothed_hit_rates_prone = smooth_data(hit_rates_prone)
        dates_prone_num = np.arange(len(dates_prone))
        hit_rates_prone_smooth = make_interp_spline(dates_prone_num, smoothed_hit_rates_prone, k=2)(dates_prone_num)
        ax.plot(dates_prone, hit_rates_prone_smooth, marker='', linestyle='-', color='#FF4500', label='Prone Hit Rate')  # Orange-rot
        has_data = True

    if show_prone_standing and hit_rate_standing_over_time:
        dates_standing, hit_rates_standing = zip(*hit_rate_standing_over_time)
        smoothed_hit_rates_standing = smooth_data(hit_rates_standing)
        dates_standing_num = np.arange(len(dates_standing))
        hit_rates_standing_smooth = make_interp_spline(dates_standing_num, smoothed_hit_rates_standing, k=2)(dates_standing_num)
        ax.plot(dates_standing, hit_rates_standing_smooth, marker='', linestyle='-', color='#32CD32', label='Standing Hit Rate')  # Leuchtend Grün
        has_data = True

    ax.set_xlabel('Date', fontsize=14, color='white', labelpad=10)
    ax.set_ylabel('Hit Rate (%)', fontsize=14, color='white', labelpad=10)
    title = 'Smoothed Hit Rate Over Time'
    if discipline_name:
        title += f' for {discipline_name}'
    ax.set_title(title, fontsize=18, color='white', weight='bold', pad=20)
    ax.tick_params(axis='x', rotation=45, labelsize=12, colors='white')
    ax.tick_params(axis='y', labelsize=12, colors='white')
    ax.legend(loc='upper left', fontsize=12, frameon=False, facecolor='black', edgecolor='black', labelcolor='white')
    ax.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.7, color='gray')

    fig.tight_layout()
    st.pyplot(fig)

def plot_discipline_comparison(discipline_stats):
    if not discipline_stats:
        st.write("No data available to plot.")
        return

    disciplines = list(discipline_stats.keys())
    hit_rates = [discipline_stats[discipline]["hit_rate"] for discipline in disciplines]

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('black')  # Hintergrund des gesamten Plots
    ax.set_facecolor('black')  # Hintergrund der Achsen

    bars = ax.bar(disciplines, hit_rates, color=['#FFD700', '#FF6347', '#7FFF00', '#1E90FF'])  # Gold, Tomatenrot, Leuchtgrün, Blau
    ax.set_title('Hit Rate Comparison Across Disciplines', fontsize=18, color='white', weight='bold', pad=20)
    ax.set_xlabel('Discipline', fontsize=14, color='white', labelpad=10)
    ax.set_ylabel('Hit Rate (%)', fontsize=14, color='white', labelpad=10)
    ax.set_ylim(0, 1)
    ax.tick_params(axis='x', labelsize=12, colors='white')
    ax.tick_params(axis='y', labelsize=12, colors='white')
    ax.bar_label(bars, fmt='%.2f', fontsize=10, color='white')
    ax.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.7, color='gray')

    fig.tight_layout()
    st.pyplot(fig)

def plot_wind_condition_comparison(wind_stats):
    if not wind_stats:
        st.write("No data available to plot.")
        return

    conditions = list(wind_stats.keys())
    hit_rates = [wind_stats[condition]["hit_rate"] for condition in conditions]

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('black')  # Hintergrund des gesamten Plots
    ax.set_facecolor('black')  # Hintergrund der Achsen

    bars = ax.bar(conditions, hit_rates, color=['#FFD700', '#FF6347', '#7FFF00', '#1E90FF'])  # Gold, Tomatenrot, Leuchtgrün, Blau
    ax.set_xlabel('Wind Conditions', fontsize=14, color='white', labelpad=10)
    ax.set_ylabel('Hit Rate (%)', fontsize=14, color='white', labelpad=10)
    ax.set_title('Hit Rate Comparison Across Wind Conditions', fontsize=18, color='white', weight='bold', pad=20)
    ax.set_ylim(0, 1)
    ax.tick_params(axis='x', labelsize=12, colors='white')
    ax.tick_params(axis='y', labelsize=12, colors='white')
    ax.bar_label(bars, fmt='%.2f', fontsize=10, color='white')
    ax.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.7, color='gray')

    fig.tight_layout()
    st.pyplot(fig)

# --- Main Fuction only for testing issues --------------------------------------------------------------------------------------------------------------
def main():
    # nur tests hier


    st.title("Biathlon Statistics")

    file_path = os.path.join("JSON", "biathlon_statistics_K_DV_01.json")
    statistics = load_statistics(file_path)

    if statistics:
        
        # schreiben dass jetzt die Hitrate geplottet wird
        st.write("Hitrate wird geplottet von allem")
        hit_rates_over_time, hit_rate_prone_over_time, hit_rate_standing_over_time = collect_hit_rates(file_path)

        #show_prone_standing = st.checkbox("Show Prone/Standing Hit Rate", value=True)
        plot_hit_rates(hit_rates_over_time, hit_rate_prone_over_time, hit_rate_standing_over_time)

        # schreiben hitrate nur alle einzelnen Disziplinen
        st.write("Hitrate wird geplottet von einzel")
        hit_rates_over_time_individual, hit_rate_prone_over_time_individual, hit_rate_standing_over_time_individual = collect_hit_rates(file_path, "Individual")
        plot_hit_rates(hit_rates_over_time_individual, hit_rate_prone_over_time_individual, hit_rate_standing_over_time_individual)

        
        st.write("Hitrate wird geplottet von Training TNS")
        hit_rates_over_time_TNS, hit_rate_prone_over_time_TNS, hit_rate_standing_over_time_TNS = collect_hit_rates(file_path, training_mode="TNS")
        plot_hit_rates(hit_rates_over_time_TNS, hit_rate_prone_over_time_TNS, hit_rate_standing_over_time_TNS)


        # Compare disciplines
        st.write("discipline comparison")
        discipline_stats = compare_disciplines(file_path)
        plot_discipline_comparison(discipline_stats)

        # Compare wind conditions globally across all disciplines
        st.write("wind condition comparison")
        wind_stats = compare_wind_conditions(file_path)
        plot_wind_condition_comparison(wind_stats)

     
        st.write("overall hit rates")
        overall_hit_rates_over_time, prone_hit_rates_over_time, standing_hit_rates_over_time = collect_overall_hit_rates(file_path)
        
        plot_overall_hit_rates(overall_hit_rates_over_time, prone_hit_rates_over_time, standing_hit_rates_over_time)


if __name__ == "__main__":
    main()

    