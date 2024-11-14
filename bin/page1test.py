import streamlit as st
import json
from datetime import datetime
import os

# Titel
st.title("Biathlon Hit Rate Calculation and Storage")

# Datumseingabe
date = st.date_input("Date of the Session")

# Abfrage nach Modus
mode = st.radio("Select the mode:", ["Training", "Competition"])

# Windbedingungen Auswahl
wind_conditions = st.selectbox("Select the wind conditions:", ["Calm", "Light Wind", "Windy", "Stormy"])

# JSON-Liste für die aktuelle Session
complete_statistics = []
total_shots = 0
total_prone_errors = 0
total_standing_errors = 0

# Weitere Auswahl bei "Training"
if mode == "Training":
    training_type = st.radio("Select training type:", ["TNS", "GLS", "Komplex"])

    if training_type == "GLS":
        # Eingabe für die Anzahl der abgegebenen Schüsse
        shots_gls = st.number_input("Number of shots fired:", min_value=1, step=1)
        st.write("Date:", date)
        # GLS Auswahl: keine weiteren Eingaben nötig für den Moment

    elif training_type == "TNS":
        # Auswahl zwischen PSPS und PPSS
        tns_discipline = st.selectbox("Select TNS discipline:", ["PSPS", "PPSS"])
        shots = 20  # TNS hat immer 20 Schüsse

        # Eingaben und Berechnungen für PSPS oder PPSS
        if tns_discipline == "PSPS":
            # PSPS: Abwechselnd liegend und stehend (prone, standing, prone, standing)
            error1 = st.number_input("Errors in 1st Shooting (prone):", min_value=0, max_value=5, step=1)
            error2 = st.number_input("Errors in 2nd Shooting (standing):", min_value=0, max_value=5, step=1)
            error3 = st.number_input("Errors in 3rd Shooting (prone):", min_value=0, max_value=5, step=1)
            error4 = st.number_input("Errors in 4th Shooting (standing):", min_value=0, max_value=5, step=1)

        elif tns_discipline == "PPSS":
            # PPSS: Zweimal liegend, dann zweimal stehend (prone, prone, standing, standing)
            error1 = st.number_input("Errors in 1st Shooting (prone):", min_value=0, max_value=5, step=1)
            error2 = st.number_input("Errors in 2nd Shooting (prone):", min_value=0, max_value=5, step=1)
            error3 = st.number_input("Errors in 3rd Shooting (standing):", min_value=0, max_value=5, step=1)
            error4 = st.number_input("Errors in 4th Shooting (standing):", min_value=0, max_value=5, step=1)

        prone_errors = error1 + (error2 if tns_discipline == "PPSS" else error3)
        standing_errors = (error3 if tns_discipline == "PPSS" else error2) + error4
        prone_hits = 10 - prone_errors
        standing_hits = 10 - standing_errors
        total_hits = prone_hits + standing_hits

        prone_hit_rate = (prone_hits / 10) * 100
        standing_hit_rate = (standing_hits / 10) * 100
        total_hit_rate = (total_hits / shots) * 100

        st.write("Total hit rate:", round(total_hit_rate, 2), "%")
        st.write("Prone hit rate:", round(prone_hit_rate, 2), "%")
        st.write("Standing hit rate:", round(standing_hit_rate, 2), "%")

        # Speichern der TNS-Statistiken in JSON-Format
        complete_statistics.append({
            "Discipline": tns_discipline,
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

    elif training_type == "Komplex":
        # Komplex: Auswahl der Disziplinen und Eingabe von Fehlern
        discipline_count = st.number_input("How many disciplines will you track?", min_value=1, step=1)
        discipline_options = ["Sprint", "Individual", "Mass Start", "Pursuit"]
        disciplines = []

        for i in range(discipline_count):
            discipline = st.selectbox(f"Select discipline {i + 1}:", discipline_options, key=f"discipline_{i}")
            disciplines.append(discipline)

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

            prone_hit_rate = (prone_hits / (shots / 2)) * 100
            standing_hit_rate = (standing_hits / (shots / 2)) * 100
            total_hit_rate = (total_hits / shots) * 100

            complete_statistics.append({
                "Discipline": discipline,
                "Instance": idx + 1,
                "Errors": {"Prone": prone_errors, "Standing": standing_errors},
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

else:
    # Competition Modus
    discipline_count = st.number_input("How many disciplines will you track?", min_value=1, step=1)
    discipline_options = ["Sprint", "Individual", "Mass Start", "Pursuit"]
    disciplines = []

    for i in range(discipline_count):
        discipline = st.selectbox(f"Select discipline {i + 1}:", discipline_options, key=f"discipline_{i}")
        disciplines.append(discipline)

    # Berechnung und Anzeige wie im Training "Komplex"-Modus
    for idx, discipline in enumerate(disciplines):
        st.subheader(f"Inputs for {discipline} (Instance {idx + 1})")
        # Analog zu vorherigen Berechnungen für jede Disziplin
    
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
st.write("Total Shots:", total_shots)
st.write("Prone Errors:", total_prone_errors)
st.write("Standing Errors:", total_standing_errors)
st.write("Overall Hit Rate:", round(overall_hit_rate, 2), "%")
st.write("Prone Hit Rate:", round(prone_hit_rate_day, 2), "%")
st.write("Standing Hit Rate:", round(standing_hit_rate_day, 2), "%")

# Daten speichern
if st.button("Save all data"):
    data = {
        "Date": date.strftime("%Y-%m-%d"),
        "Mode": mode,
        "Wind Conditions": wind_conditions,
        "Statistics": complete_statistics,
        "Daily Summary": {
            "Total Shots": total_shots,
            "Total Prone Errors": total_prone_errors,
            "Total Standing Errors": total_standing_errors,
            "Overall Hit Rate": round(overall_hit_rate, 2),
            "Prone Hit Rate": round(prone_hit_rate_day, 2),
            "Standing Hit Rate": round(standing_hit_rate_day, 2)
        }
    }

    # Datei Pfad und Speicherprozess
    filename = f"biathlon_data_{date.strftime('%Y-%m-%d')}.json"
    filepath = os.path.join("biathlon_sessions", filename)
    os.makedirs("biathlon_sessions", exist_ok=True)
    
    with open(filepath, "w") as outfile:
        json.dump(data, outfile, indent=4)

    st.success(f"Data saved as {filename} in the 'biathlon_sessions' directory.")
