import json
import os
import streamlit as st

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


def main():
    st.title("Biathlon Statistics")

    file_path = os.path.join("JSON", "biathlon_statistics_K_DV_01.json")
    statistics = load_statistics(file_path)

    if statistics:
        total_shots = calculate_total_shots(statistics)
        total_prone_errors = calculate_prone_errors(statistics)
        total_standing_errors = calculate_standing_errors(statistics)

        overall_hit_rate, prone_hit_rate, standing_hit_rate = calculate_hit_rate(total_shots, total_prone_errors, total_standing_errors)


        
        st.write(f"Total shots made: {total_shots}")
        st.write(f"Total prone errors: {total_prone_errors}")
        st.write(f"Total standing errors: {total_standing_errors}")
        st.write(f"Overall hit rate: {overall_hit_rate:.2f}")
        st.write(f"Prone hit rate: {prone_hit_rate:.2f}")
        st.write(f"Standing hit rate: {standing_hit_rate:.2f}")
        
    main()