import streamlit as st
import json
from datetime import datetime
import os
from functions import biathlon_statistics

# Titel
st.title("Biathlon Hit Rate Calculation and Storage")

# Datumseingabe
date = st.date_input("Date of the Session")

# Abfrage nach Modus
mode = st.radio("Select the mode:", ["Training", "Competition"])

#wenn competetition ausgewählt, dann alles nachfolgende ausführen
if mode == "Competition":
        
    # Windbedingungen Auswahl
    wind_conditions = st.selectbox("Select the wind conditions:", ["Calm", "Light Wind", "Windy", "Stormy"])


    # Auswahl der Disziplin(en)
    discipline_count = st.number_input("How many disciplines will you track?", min_value=1, step=1)
    discipline_options = ["Sprint", "Individual", "Mass Start", "Pursuit"]
    disciplines = []

    for i in range(discipline_count):
        discipline = st.selectbox(f"Select discipline {i + 1}:", discipline_options, key=f"discipline_{i}")
        disciplines.append(discipline)

    # JSON-Liste für die aktuelle Session
    complete_statistics = []
    total_shots = 0
    total_prone_errors = 0
    total_standing_errors = 0

    # Eingaben und Berechnungen für jede ausgewählte Disziplin
    for idx, discipline in enumerate(disciplines):
        st.subheader(f"Inputs for {discipline} (Instance {idx + 1})")

        if discipline == "Sprint":
            cols = st.columns(2)
            error1 = cols[0].number_input("Errors in 1st Shooting (prone):", min_value=0, max_value=5, step=1, key=f"error1_{discipline}_{idx}")
            error2 = cols[1].number_input("Errors in 2nd Shooting (standing):", min_value=0, max_value=5, step=1, key=f"error2_{discipline}_{idx}")

            shots = 10
            prone_errors = error1
            standing_errors = error2
            prone_hits = 5 - prone_errors
            standing_hits = 5 - standing_errors
            total_hits = prone_hits + standing_hits

        elif discipline == "Individual":
            cols = st.columns(4)
            error1 = cols[0].number_input("Errors in 1st Shooting (prone):", min_value=0, max_value=5, step=1, key=f"error1_{discipline}_{idx}")
            error2 = cols[1].number_input("Errors in 2nd Shooting (standing):", min_value=0, max_value=5, step=1, key=f"error2_{discipline}_{idx}")
            error3 = cols[2].number_input("Errors in 3rd Shooting (prone):", min_value=0, max_value=5, step=1, key=f"error3_{discipline}_{idx}")
            error4 = cols[3].number_input("Errors in 4th Shooting (standing):", min_value=0, max_value=5, step=1, key=f"error4_{discipline}_{idx}")

            shots = 20
            prone_errors = error1 + error3
            standing_errors = error2 + error4
            prone_hits = 10 - prone_errors
            standing_hits = 10 - standing_errors
            total_hits = prone_hits + standing_hits

        elif discipline in ["Mass Start", "Pursuit"]:
            cols = st.columns(4)
            error1 = cols[0].number_input("Errors in 1st Shooting (prone):", min_value=0, max_value=5, step=1, key=f"error1_{discipline}_{idx}")
            error2 = cols[1].number_input("Errors in 2nd Shooting (prone):", min_value=0, max_value=5, step=1, key=f"error2_{discipline}_{idx}")
            error3 = cols[2].number_input("Errors in 3rd Shooting (standing):", min_value=0, max_value=5, step=1, key=f"error3_{discipline}_{idx}")
            error4 = cols[3].number_input("Errors in 4th Shooting (standing):", min_value=0, max_value=5, step=1, key=f"error4_{discipline}_{idx}")

            shots = 20
            prone_errors = error1 + error2
            standing_errors = error3 + error4
            prone_hits = 10 - prone_errors
            standing_hits = 10 - standing_errors
            total_hits = prone_hits + standing_hits

        prone_hit_rate = (prone_hits / (shots / 2)) * 100
        standing_hit_rate = (standing_hits / (shots / 2)) * 100
        total_hit_rate = (total_hits / shots) * 100

        #st.write(f"**Results for {discipline} (Instance {idx + 1}):**")
        #st.write("Total hit rate:", round(total_hit_rate, 2), "%")
        #st.write("Prone hit rate:", round(prone_hit_rate, 2), "%")
        #st.write("Standing hit rate:", round(standing_hit_rate, 2), "%")
        
        

        # Einzelne Disziplinstatistiken speichern
        complete_statistics.append({
            "Discipline": discipline,
            "Instance": idx + 1,
            "Errors": {
                "Prone": prone_errors,
                "Standing": standing_errors
            },
            "Hit Rates": {
                "Total": round(total_hit_rate, 2),
                "Prone": round(prone_hit_rate, 2),
                "Standing": round(standing_hit_rate, 2),
            }
        })

        # Tagesstatistik aktualisieren
        total_shots += shots
        total_prone_errors += prone_errors
        total_standing_errors += standing_errors

    # Berechnung der Tagesstatistik, nur wenn Werte vorhanden sind
    if total_shots > 0:
        total_errors = total_prone_errors + total_standing_errors
        overall_hit_rate = ((total_shots - total_errors) / total_shots) * 100
        prone_hit_rate_day = ((total_shots // 2 - total_prone_errors) / (total_shots // 2)) * 100
        standing_hit_rate_day = ((total_shots // 2 - total_standing_errors) / (total_shots // 2)) * 100
    else:
        overall_hit_rate = prone_hit_rate_day = standing_hit_rate_day = 0

    # Tageszusammenfassung anzeigen
    st.write(f"**Daily Summary ({date.strftime('%Y-%m-%d')}):**")
    st.write("Total shots:", total_shots)
    st.write("Total prone errors:", total_prone_errors)
    st.write("Total standing errors:", total_standing_errors)
    st.write("Overall hit rate:", round(overall_hit_rate, 2), "%")
    st.write("Prone hit rate for the day:", round(prone_hit_rate_day, 2), "%")
    st.write("Standing hit rate for the day:", round(standing_hit_rate_day, 2), "%")

    # JSON-Datei laden oder initialisieren, falls nicht vorhanden
    if st.button("Save all data"):
        if os.path.exists("biathlon_statistics.json") and os.path.getsize("biathlon_statistics.json") > 0:
            with open("biathlon_statistics.json", "r") as file:
                try:
                    statistics = json.load(file)
                except json.JSONDecodeError:
                    statistics = []
        else:
            statistics = []

        # Speichern der neuen Daten
        statistics.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Mode": mode,
            "Trainings_mode": "Komplex",
            "Wind Conditions": wind_conditions,
            "Daily Summary": {
                "Total Shots": total_shots,
                "Prone Errors": total_prone_errors,
                "Standing Errors": total_standing_errors,
                "Overall Hit Rate": round(overall_hit_rate, 2),
                "Prone Hit Rate": round(prone_hit_rate_day, 2),
                "Standing Hit Rate": round(standing_hit_rate_day, 2)
            },
            "Discipline Details": complete_statistics
        })

        # Daten in die JSON-Datei schreiben
        with open("biathlon_statistics.json", "w") as file:
            json.dump(statistics, file, indent=4)
            st.success("Data saved successfully!")

#wenn training ausgewählt, dann alles nachfolgende ausführen
else:
    mode = "Training"
    #auswahl TNS GLS oder Komplex
    training_mode = st.radio("Select the training mode:", ["TNS", "GLS", "Komplex"])

    if training_mode == "Komplex":
        biathlon_statistics(date, mode)
    elif training_mode == "TNS":
        st.write("TNS mode selected.")

        
    else:
        st.write("GLS mode selected.")
         #chris GLS Code

