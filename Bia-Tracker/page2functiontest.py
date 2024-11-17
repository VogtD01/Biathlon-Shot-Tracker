def analyze_discipline_old(file_path, discipline_name):
    statistics = load_statistics(file_path)
    if not statistics:
        return None, None, None, None, None, None, None

    discipline_count = 0
    total_shots = 0
    total_prone_errors = 0
    total_standing_errors = 0

    # Setze die Anzahl der Schüsse pro Instanz basierend auf der Disziplin
    shots_per_instance = 10 if discipline_name == "Sprint" else 20

    for entry in statistics:
        if "Discipline Details" in entry:
            for discipline in entry["Discipline Details"]:
                if discipline["Discipline"] == discipline_name:
                    discipline_count += 1
                    total_shots += shots_per_instance
                    total_prone_errors += discipline["Errors"]["Prone"]
                    total_standing_errors += discipline["Errors"]["Standing"]

    if total_shots > 0:
        hit_rate = 1 - (total_prone_errors + total_standing_errors) / total_shots
        hit_rate_prone = 1 - total_prone_errors / (total_shots / 2)
        hit_rate_standing = 1 - total_standing_errors / (total_shots / 2)
    else:
        hit_rate = hit_rate_prone = hit_rate_standing = 0

    return discipline_count, total_shots, total_prone_errors, total_standing_errors, hit_rate, hit_rate_prone, hit_rate_standing
#############################

def analyze_discipline(file_path, discipline_name, mode=None): #mode is none wenn gesamtstatistik berechnet wird, sonst "Training" oder "Competition"
    statistics = load_statistics(file_path)
    if not statistics:
        return None, None, None, None, None, None, None

    discipline_count = 0
    total_shots = 0
    total_prone_errors = 0
    total_standing_errors = 0

    # Setze die Anzahl der Schüsse pro Instanz basierend auf der Disziplin
    shots_per_instance = 10 if discipline_name == "Sprint" else 20

    for entry in statistics:
        if "Discipline Details" in entry:
            for discipline in entry["Discipline Details"]:
                if discipline["Discipline"] == discipline_name:
                    if mode is None or entry["Mode"] == mode:
                        discipline_count += 1
                        total_shots += shots_per_instance
                        total_prone_errors += discipline["Errors"]["Prone"]
                        total_standing_errors += discipline["Errors"]["Standing"]

    if total_shots > 0:
        hit_rate = 1 - (total_prone_errors + total_standing_errors) / total_shots
        hit_rate_prone = 1 - total_prone_errors / (total_shots / 2)
        hit_rate_standing = 1 - total_standing_errors / (total_shots / 2)
    else:
        hit_rate = hit_rate_prone = hit_rate_standing = 0

    return discipline_count, total_shots, total_prone_errors, total_standing_errors, hit_rate, hit_rate_prone, hit_rate_standing
################################

def collect_hit_rates_old(file_path, discipline_name, mode=None, training_mode=None):
    statistics = load_statistics(file_path)
    if not statistics:
        return [], [], []

    hit_rates_over_time = []
    hit_rate_prone_over_time = []
    hit_rate_standing_over_time = []

    # Setze die Anzahl der Schüsse pro Instanz basierend auf der Disziplin
    shots_per_instance = 10 if discipline_name == "Sprint" else 20

    for entry in statistics:
        if "Discipline Details" in entry:
            for discipline in entry["Discipline Details"]:
                if discipline["Discipline"] == discipline_name:
                    if (mode is None or entry["Mode"] == mode) and (training_mode is None or entry["Trainings_mode"] == training_mode):
                        total_shots = shots_per_instance
                        total_prone_errors = discipline["Errors"]["Prone"]
                        total_standing_errors = discipline["Errors"]["Standing"]

                        if total_shots > 0:
                            hit_rate = 1 - (total_prone_errors + total_standing_errors) / total_shots
                            hit_rate_prone = 1 - total_prone_errors / (total_shots / 2)
                            hit_rate_standing = 1 - total_standing_errors / (total_shots / 2)
                        else:
                            hit_rate = hit_rate_prone = hit_rate_standing = 0

                        hit_rates_over_time.append((entry["Date"], hit_rate))
                        hit_rate_prone_over_time.append((entry["Date"], hit_rate_prone))
                        hit_rate_standing_over_time.append((entry["Date"], hit_rate_standing))

    return hit_rates_over_time, hit_rate_prone_over_time, hit_rate_standing_over_time
