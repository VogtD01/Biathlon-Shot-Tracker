import streamlit as st
import json
from datetime import datetime
import os
from functions import biathlon_stats_komplex, biathlon_stats_gls    


def page1():
    # Titel
    st.title("Biathlon Hit Rate Calculation and Storage")

    # Datumseingabe
    date = st.date_input("Date of the Session")

    # Abfrage nach Modus
    mode = st.radio("Select the mode:", ["Training", "Competition"])

    #wenn competetition ausgewählt, dann alles nachfolgende ausführen
    if mode == "Competition": 
        training_mode = "Komplex"
        biathlon_stats_komplex(date, mode, training_mode)

    #wenn training ausgewählt, dann alles nachfolgende ausführen
    else:
        mode = "Training"
        #auswahl TNS GLS oder Komplex
        training_mode = st.radio("Select the training mode:", ["TNS", "GLS", "Komplex"])

        if training_mode == "Komplex":
            biathlon_stats_komplex(date, mode, training_mode)
        elif training_mode == "TNS":
            biathlon_stats_komplex(date, mode, training_mode)
            
        else:
            training_mode = "GLS"
            biathlon_stats_gls(date, mode, training_mode)

