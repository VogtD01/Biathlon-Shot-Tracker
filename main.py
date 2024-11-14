import streamlit as st
import json
from datetime import datetime

# Title
st.title("Biathlon Hit Rate Calculation and Storage")

# Date input
date = st.date_input("Date of the competition")

# Input fields for the number of errors in eight shootings (alternating prone and standing)
error1 = st.number_input("Errors in 1st shooting (prone):", min_value=0, max_value=5, step=1)
error2 = st.number_input("Errors in 2nd shooting (standing):", min_value=0, max_value=5, step=1)
error3 = st.number_input("Errors in 3rd shooting (prone):", min_value=0, max_value=5, step=1)
error4 = st.number_input("Errors in 4th shooting (standing):", min_value=0, max_value=5, step=1)
error5 = st.number_input("Errors in 5th shooting (prone):", min_value=0, max_value=5, step=1)
error6 = st.number_input("Errors in 6th shooting (standing):", min_value=0, max_value=5, step=1)
error7 = st.number_input("Errors in 7th shooting (prone):", min_value=0, max_value=5, step=1)
error8 = st.number_input("Errors in 8th shooting (standing):", min_value=0, max_value=5, step=1)

# Button for calculation
if st.button("Calculate and save hit rate"):
    # Calculate total number of shots and misses
    total_shots = 40  # 8 shootings * 5 shots per shooting
    prone_errors = error1 + error3 + error5 + error7
    standing_errors = error2 + error4 + error6 + error8
    
    # Calculate hits
    prone_hits = (20 - prone_errors)  # 4 prone shootings * 5 shots
    standing_hits = (20 - standing_errors)  # 4 standing shootings * 5 shots
    total_hits = prone_hits + standing_hits
    
    # Calculate hit rate
    prone_hit_rate = (prone_hits / 20) * 100
    standing_hit_rate = (standing_hits / 20) * 100
    total_hit_rate = (total_hits / total_shots) * 100
    
    # Display results
    st.write("The total hit rate is:", round(total_hit_rate, 2), "%")
    st.write("Hit rate prone:", round(prone_hit_rate, 2), "%")
    st.write("Hit rate standing:", round(standing_hit_rate, 2), "%")
    
    # Save data in a dictionary
    data = {
        "Date": date.strftime("%Y-%m-%d"),
        "Errors": {
            "Shooting 1 (prone)": error1,
            "Shooting 2 (standing)": error2,
            "Shooting 3 (prone)": error3,
            "Shooting 4 (standing)": error4,
            "Shooting 5 (prone)": error5,
            "Shooting 6 (standing)": error6,
            "Shooting 7 (prone)": error7,
            "Shooting 8 (standing)": error8,
        },
        "Hit Rates": {
            "Total": round(total_hit_rate, 2),
            "Prone": round(prone_hit_rate, 2),
            "Standing": round(standing_hit_rate, 2),
        }
    }
    
    # Load JSON file and append data
    try:
        with open("biathlon_statistics.json", "r") as file:
            statistics = json.load(file)
    except FileNotFoundError:
        statistics = []
        
    statistics.append(data)
    
    # Save updated data in JSON file
    with open("biathlon_statistics.json", "w") as file:
        json.dump(statistics, file, indent=4)
    
    st.success("The hit rate and data were successfully saved.")
