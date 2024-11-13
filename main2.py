import streamlit as st
import json
from datetime import datetime
import os

# Titel
st.title("Biathlon Trefferquote Berechnung und Speicherung")

# Datumseingabe
datum = st.date_input("Datum des Wettkampfs")

# Auswahl der Disziplin(en)
disziplinen = st.multiselect(
    "Wähle die Disziplin(en):",
    ["Sprint", "Einzel", "Massenstart", "Verfolgung"]
)

# JSON-Liste für das aktuelle Datum
gesamte_statistik = []

# Eingabe und Berechnung für jede ausgewählte Disziplin
for disziplin in disziplinen:
    st.subheader(f"Eingaben für {disziplin}")

    if disziplin == "Sprint":
        fehler1 = st.number_input("Fehler im 1. Schießen (liegend) - Sprint:", min_value=0, max_value=5, step=1, key=f"fehler1_{disziplin}")
        fehler2 = st.number_input("Fehler im 2. Schießen (stehend) - Sprint:", min_value=0, max_value=5, step=1, key=f"fehler2_{disziplin}")
        
        gesamt_schuesse = 10
        liegend_fehler = fehler1
        stehend_fehler = fehler2
        liegend_treffer = 5 - liegend_fehler
        stehend_treffer = 5 - stehend_fehler
        gesamttreffer = liegend_treffer + stehend_treffer

    elif disziplin == "Einzel":
        fehler1 = st.number_input("Fehler im 1. Schießen (liegend) - Einzel:", min_value=0, max_value=5, step=1, key=f"fehler1_{disziplin}")
        fehler2 = st.number_input("Fehler im 2. Schießen (stehend) - Einzel:", min_value=0, max_value=5, step=1, key=f"fehler2_{disziplin}")
        fehler3 = st.number_input("Fehler im 3. Schießen (liegend) - Einzel:", min_value=0, max_value=5, step=1, key=f"fehler3_{disziplin}")
        fehler4 = st.number_input("Fehler im 4. Schießen (stehend) - Einzel:", min_value=0, max_value=5, step=1, key=f"fehler4_{disziplin}")

        gesamt_schuesse = 20
        liegend_fehler = fehler1 + fehler3
        stehend_fehler = fehler2 + fehler4
        liegend_treffer = 10 - liegend_fehler
        stehend_treffer = 10 - stehend_fehler
        gesamttreffer = liegend_treffer + stehend_treffer

    elif disziplin == "Massenstart":
        fehler1 = st.number_input("Fehler im 1. Schießen (liegend) - Massenstart:", min_value=0, max_value=5, step=1, key=f"fehler1_{disziplin}")
        fehler2 = st.number_input("Fehler im 2. Schießen (liegend) - Massenstart:", min_value=0, max_value=5, step=1, key=f"fehler2_{disziplin}")
        fehler3 = st.number_input("Fehler im 3. Schießen (stehend) - Massenstart:", min_value=0, max_value=5, step=1, key=f"fehler3_{disziplin}")
        fehler4 = st.number_input("Fehler im 4. Schießen (stehend) - Massenstart:", min_value=0, max_value=5, step=1, key=f"fehler4_{disziplin}")

        gesamt_schuesse = 20
        liegend_fehler = fehler1 + fehler2
        stehend_fehler = fehler3 + fehler4
        liegend_treffer = 10 - liegend_fehler
        stehend_treffer = 10 - stehend_fehler
        gesamttreffer = liegend_treffer + stehend_treffer

    elif disziplin == "Verfolgung":
        fehler1 = st.number_input("Fehler im 1. Schießen (liegend) - Verfolgung:", min_value=0, max_value=5, step=1, key=f"fehler1_{disziplin}")
        fehler2 = st.number_input("Fehler im 2. Schießen (liegend) - Verfolgung:", min_value=0, max_value=5, step=1, key=f"fehler2_{disziplin}")
        fehler3 = st.number_input("Fehler im 3. Schießen (stehend) - Verfolgung:", min_value=0, max_value=5, step=1, key=f"fehler3_{disziplin}")
        fehler4 = st.number_input("Fehler im 4. Schießen (stehend) - Verfolgung:", min_value=0, max_value=5, step=1, key=f"fehler4_{disziplin}")

        gesamt_schuesse = 20
        liegend_fehler = fehler1 + fehler2
        stehend_fehler = fehler3 + fehler4
        liegend_treffer = 10 - liegend_fehler
        stehend_treffer = 10 - stehend_fehler
        gesamttreffer = liegend_treffer + stehend_treffer

    liegend_trefferquote = (liegend_treffer / (gesamt_schuesse / 2)) * 100
    stehend_trefferquote = (stehend_treffer / (gesamt_schuesse / 2)) * 100
    gesamttrefferquote = (gesamttreffer / gesamt_schuesse) * 100

    st.write(f"**Ergebnisse für {disziplin}:**")
    st.write("Die Gesamttrefferquote beträgt:", round(gesamttrefferquote, 2), "%")
    st.write("Trefferquote liegend:", round(liegend_trefferquote, 2), "%")
    st.write("Trefferquote stehend:", round(stehend_trefferquote, 2), "%")

    daten = {
        "Datum": datum.strftime("%Y-%m-%d"),
        "Disziplin": disziplin,
        "Fehler": {
            "Liegend": liegend_fehler,
            "Stehend": stehend_fehler
        },
        "Trefferquoten": {
            "Gesamt": round(gesamttrefferquote, 2),
            "Liegend": round(liegend_trefferquote, 2),
            "Stehend": round(stehend_trefferquote, 2),
        }
    }

    gesamte_statistik.append(daten)

# JSON-Datei laden und initialisieren, falls sie nicht existiert oder leer ist
if st.button("Speichere alle Daten"):
    if os.path.exists("biathlon_statistik.json") and os.path.getsize("biathlon_statistik.json") > 0:
        with open("biathlon_statistik.json", "r") as file:
            try:
                statistik = json.load(file)
            except json.JSONDecodeError:
                statistik = []
    else:
        statistik = []

    statistik.append({
        "Datum": datum.strftime("%Y-%m-%d"),
        "Statistik": gesamte_statistik
    })

    with open("biathlon_statistik.json", "w") as file:
        json.dump(statistik, file, indent=4)

    st.success("Die Trefferquote und Daten wurden erfolgreich gespeichert.")
