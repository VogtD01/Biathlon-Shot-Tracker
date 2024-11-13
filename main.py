import streamlit as st
import json
from datetime import datetime

# Titel
st.title("Biathlon Trefferquote Berechnung und Speicherung")

# Datumseingabe
datum = st.date_input("Datum des Wettkampfs")

# Eingabefelder für die Anzahl der Fehler bei acht Schießen (abwechselnd liegend und stehend)
fehler1 = st.number_input("Fehler im 1. Schießen (liegend):", min_value=0, max_value=5, step=1)
fehler2 = st.number_input("Fehler im 2. Schießen (stehend):", min_value=0, max_value=5, step=1)
fehler3 = st.number_input("Fehler im 3. Schießen (liegend):", min_value=0, max_value=5, step=1)
fehler4 = st.number_input("Fehler im 4. Schießen (stehend):", min_value=0, max_value=5, step=1)
fehler5 = st.number_input("Fehler im 5. Schießen (liegend):", min_value=0, max_value=5, step=1)
fehler6 = st.number_input("Fehler im 6. Schießen (stehend):", min_value=0, max_value=5, step=1)
fehler7 = st.number_input("Fehler im 7. Schießen (liegend):", min_value=0, max_value=5, step=1)
fehler8 = st.number_input("Fehler im 8. Schießen (stehend):", min_value=0, max_value=5, step=1)

# Button zur Berechnung
if st.button("Berechne und speichere Trefferquote"):
    # Gesamtanzahl an Schüssen und Fehlschüssen berechnen
    gesamt_schuesse = 40  # 8 Schießen * 5 Schüsse pro Schießen
    liegend_fehler = fehler1 + fehler3 + fehler5 + fehler7
    stehend_fehler = fehler2 + fehler4 + fehler6 + fehler8
    
    # Treffer berechnen
    liegend_treffer = (20 - liegend_fehler)  # 4 liegende Schießen * 5 Schüsse
    stehend_treffer = (20 - stehend_fehler)  # 4 stehende Schießen * 5 Schüsse
    gesamttreffer = liegend_treffer + stehend_treffer
    
    # Trefferquote berechnen
    liegend_trefferquote = (liegend_treffer / 20) * 100
    stehend_trefferquote = (stehend_treffer / 20) * 100
    gesamttrefferquote = (gesamttreffer / gesamt_schuesse) * 100
    
    # Ergebnisse anzeigen
    st.write("Die Gesamttrefferquote beträgt:", round(gesamttrefferquote, 2), "%")
    st.write("Trefferquote liegend:", round(liegend_trefferquote, 2), "%")
    st.write("Trefferquote stehend:", round(stehend_trefferquote, 2), "%")
    
    # Daten in einem Dictionary speichern
    daten = {
        "Datum": datum.strftime("%Y-%m-%d"),
        "Fehler": {
            "Schießen 1 (liegend)": fehler1,
            "Schießen 2 (stehend)": fehler2,
            "Schießen 3 (liegend)": fehler3,
            "Schießen 4 (stehend)": fehler4,
            "Schießen 5 (liegend)": fehler5,
            "Schießen 6 (stehend)": fehler6,
            "Schießen 7 (liegend)": fehler7,
            "Schießen 8 (stehend)": fehler8,
        },
        "Trefferquoten": {
            "Gesamt": round(gesamttrefferquote, 2),
            "Liegend": round(liegend_trefferquote, 2),
            "Stehend": round(stehend_trefferquote, 2),
        }
    }
    
    # JSON-Datei laden und Daten anhängen
    try:
        with open("biathlon_statistik.json", "r") as file:
            statistik = json.load(file)
    except FileNotFoundError:
        statistik = []
        
    statistik.append(daten)
    
    # Aktualisierte Daten in JSON-Datei speichern
    with open("biathlon_statistik.json", "w") as file:
        json.dump(statistik, file, indent=4)
    
    st.success("Die Trefferquote und Daten wurden erfolgreich gespeichert.")
