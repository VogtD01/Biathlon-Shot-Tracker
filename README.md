# Biathlon-Shot-Tracker
Dokumentation Shooting Data Biathlon

## Voraussetzungen

- **Python 3.7 oder höher** muss installiert sein. [Python herunterladen](https://www.python.org/downloads/)

## Installation und Ausführung

Hier sind die Schritte, um die Anwendung auf Ihrem lokalen Computer auszuführen:

1. **Projekt herunterladen**

   Laden Sie den Projektordner von GitHub herunter oder klonen Sie das Repository:
   ```sh
   git clone https://github.com/VogtD01/Biathlon-Shot-Tracker.git
   ```

2. **Ordner öffnen**

   Navigieren Sie zu dem heruntergeladenen Projektordner:
   ```sh
   cd Biathlon-Shot-Tracker
   ```

3. **Virtuelle Umgebung erstellen**

   Erstellen Sie eine neue Python-Umgebung:
   ```sh
   python -m venv .venv
   ```

4. **Virtuelle Umgebung aktivieren**

   Aktivieren Sie die virtuelle Umgebung:

   **Windows:**
   ```sh
   .venv\Scripts\Activate
   ```

   **Linux/Mac:**
   ```sh
   source .venv/bin/activate
   ```

5. **Abhängigkeiten installieren**

   Installieren Sie die erforderlichen Pakete mittels:
   ```sh
   pip install -r requirements.txt
   ```

6. **Anwendung starten**

   Starten Sie die Anwendung mit dem folgenden Befehl:
   ```sh
   streamlit run app.py
   ```

7. **Beispieldaten ansehen**
   Verwenden Sie das Athleten-Login oder das Trainer-Login, um bereits eingegebene Daten ansehen zu können:

   **Zugangsdaten Athlet:**
   - **Email:** dominic@biathlontracker.de
   - **Passwort:** 2601

   **Zugangsdaten Trainer:**
   - **Email:** huber@gmail.de
   - **Passwort:** test

8. Die Seite kann alternativ auch über den folgenden Link direkt ohne lokale Entwicklungsumgebung aufgerufen werden:
   [Biathlon Shot Tracker](https://biathlon-shot-tracker-nugzjq9knyderdqrtt5yfm.streamlit.app/)