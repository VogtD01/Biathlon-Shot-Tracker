import streamlit as st
import json
from datetime import datetime
import os

# Title
st.title("Biathlon Hit Rate Calculation and Storage")

# Date input
date = st.date_input("Date of the Competition")

# Selection of the discipline(s)
disciplines = st.multiselect(
    "Select the discipline(s):",
    ["Sprint", "Individual", "Mass Start", "Pursuit"]
)

# JSON list for the current date
complete_statistics = []

# Input and calculation for each selected discipline
for discipline in disciplines:
    st.subheader(f"Inputs for {discipline}")

    if discipline == "Sprint":
        error1 = st.number_input("Errors in the 1st Shooting (prone) - Sprint:", min_value=0, max_value=5, step=1, key=f"error1_{discipline}")
        error2 = st.number_input("Errors in the 2nd Shooting (standing) - Sprint:", min_value=0, max_value=5, step=1, key=f"error2_{discipline}")
        
        total_shots = 10
        prone_errors = error1
        standing_errors = error2
        prone_hits = 5 - prone_errors
        standing_hits = 5 - standing_errors
        total_hits = prone_hits + standing_hits

    elif discipline == "Individual":
        error1 = st.number_input("Errors in the 1st Shooting (prone) - Individual:", min_value=0, max_value=5, step=1, key=f"error1_{discipline}")
        error2 = st.number_input("Errors in the 2nd Shooting (standing) - Individual:", min_value=0, max_value=5, step=1, key=f"error2_{discipline}")
        error3 = st.number_input("Errors in the 3rd Shooting (prone) - Individual:", min_value=0, max_value=5, step=1, key=f"error3_{discipline}")
        error4 = st.number_input("Errors in the 4th Shooting (standing) - Individual:", min_value=0, max_value=5, step=1, key=f"error4_{discipline}")

        total_shots = 20
        prone_errors = error1 + error3
        standing_errors = error2 + error4
        prone_hits = 10 - prone_errors
        standing_hits = 10 - standing_errors
        total_hits = prone_hits + standing_hits

    elif discipline == "Mass Start":
        error1 = st.number_input("Errors in the 1st Shooting (prone) - Mass Start:", min_value=0, max_value=5, step=1, key=f"error1_{discipline}")
        error2 = st.number_input("Errors in the 2nd Shooting (prone) - Mass Start:", min_value=0, max_value=5, step=1, key=f"error2_{discipline}")
        error3 = st.number_input("Errors in the 3rd Shooting (standing) - Mass Start:", min_value=0, max_value=5, step=1, key=f"error3_{discipline}")
        error4 = st.number_input("Errors in the 4th Shooting (standing) - Mass Start:", min_value=0, max_value=5, step=1, key=f"error4_{discipline}")

        total_shots = 20
        prone_errors = error1 + error2
        standing_errors = error3 + error4
        prone_hits = 10 - prone_errors
        standing_hits = 10 - standing_errors
        total_hits = prone_hits + standing_hits

    elif discipline == "Pursuit":
        error1 = st.number_input("Errors in the 1st Shooting (prone) - Pursuit:", min_value=0, max_value=5, step=1, key=f"error1_{discipline}")
        error2 = st.number_input("Errors in the 2nd Shooting (prone) - Pursuit:", min_value=0, max_value=5, step=1, key=f"error2_{discipline}")
        error3 = st.number_input("Errors in the 3rd Shooting (standing) - Pursuit:", min_value=0, max_value=5, step=1, key=f"error3_{discipline}")
        error4 = st.number_input("Errors in the 4th Shooting (standing) - Pursuit:", min_value=0, max_value=5, step=1, key=f"error4_{discipline}")

        total_shots = 20
        prone_errors = error1 + error2
        standing_errors = error3 + error4
        prone_hits = 10 - prone_errors
        standing_hits = 10 - standing_errors
        total_hits = prone_hits + standing_hits

    prone_hit_rate = (prone_hits / (total_shots / 2)) * 100
    standing_hit_rate = (standing_hits / (total_shots / 2)) * 100
    total_hit_rate = (total_hits / total_shots) * 100

    st.write(f"**Results for {discipline}:**")
    st.write("The total hit rate is:", round(total_hit_rate, 2), "%")
    st.write("Prone hit rate:", round(prone_hit_rate, 2), "%")
    st.write("Standing hit rate:", round(standing_hit_rate, 2), "%")

    data = {
        "Date": date.strftime("%Y-%m-%d"),
        "Discipline": discipline,
        "Errors": {
            "Prone": prone_errors,
            "Standing": standing_errors
        },
        "Hit Rates": {
            "Total": round(total_hit_rate, 2),
            "Prone": round(prone_hit_rate, 2),
            "Standing": round(standing_hit_rate, 2),
        }
    }

    complete_statistics.append(data)

# Load JSON file and initialize if it does not exist or is empty
if st.button("Save all data"):
    if os.path.exists("biathlon_statistics.json") and os.path.getsize("biathlon_statistics.json") > 0:
        with open("biathlon_statistics.json", "r") as file:
            try:
                statistics = json.load(file)
            except json.JSONDecodeError:
                statistics = []
    else:
        statistics = []

    statistics.append({
        "Date": date.strftime("%Y-%m-%d"),
        "Statistics": complete_statistics
    })

    with open("biathlon_statistics.json", "w") as file:
        json.dump(statistics, file, indent=4)

    st.success("Hit rate and data were saved successfully.")
