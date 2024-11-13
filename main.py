import streamlit as st

# Titel
st.title("Durchschnittsberechnung")

# Eingabefelder für fünf Zahlen
zahl1 = st.number_input("Gib die erste Zahl ein:", step=1.0)
zahl2 = st.number_input("Gib die zweite Zahl ein:", step=1.0)
zahl3 = st.number_input("Gib die dritte Zahl ein:", step=1.0)
zahl4 = st.number_input("Gib die vierte Zahl ein:", step=1.0)
zahl5 = st.number_input("Gib die fünfte Zahl ein:", step=1.0)

# Button zur Berechnung
if st.button("Berechne Durchschnitt"):
    # Durchschnitt berechnen
    durchschnitt = (zahl1 + zahl2 + zahl3 + zahl4 + zahl5) / 5
    st.write("Der Durchschnitt der eingegebenen Zahlen ist:", durchschnitt)