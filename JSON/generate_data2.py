import json
import random
from datetime import datetime, timedelta

def generate_random_data(start_date, end_date, file_path):
    modes = ["Training", "Competition"]
    training_modes = ["TNS", "Komplex"]
    wind_conditions = ["Calm", "Light Wind", "Windy", "Stormy"]
    disciplines = ["Individual", "Mass Start", "Sprint", "Pursuit"]

    data = []
    current_date = start_date

    while current_date <= end_date:
        num_entries = random.randint(2, 4)
        for _ in range(num_entries):
            mode = random.choice(modes)
            training_mode = random.choice(training_modes) if mode == "Training" else None
            wind_condition = random.choice(wind_conditions)

            total_shots = 40
            prone_errors = random.randint(0, 5)
            standing_errors = random.randint(0, 5)
            overall_hit_rate = 100 - ((prone_errors + standing_errors) / total_shots * 100)
            prone_hit_rate = 100 - (prone_errors / (total_shots / 2) * 100)
            standing_hit_rate = 100 - (standing_errors / (total_shots / 2) * 100)

            # Adjust hit rates to be mostly in the range of 70%-100%
            overall_hit_rate = max(70, min(overall_hit_rate, 100))
            prone_hit_rate = max(70, min(prone_hit_rate, 100))
            standing_hit_rate = max(70, min(standing_hit_rate, 100))

            discipline_details = []
            num_disciplines = 1 if mode == "Competition" else random.randint(1, 3)
            for i in range(num_disciplines):
                discipline = random.choice(disciplines)
                shots_per_instance = 10 if discipline == "Sprint" else 20
                prone_errors_discipline = random.randint(0, shots_per_instance // 2)
                standing_errors_discipline = random.randint(0, shots_per_instance // 2)
                total_errors_discipline = prone_errors_discipline + standing_errors_discipline
                hit_rate_discipline = 100 - (total_errors_discipline / shots_per_instance * 100)
                hit_rate_prone_discipline = 100 - (prone_errors_discipline / (shots_per_instance / 2) * 100)
                hit_rate_standing_discipline = 100 - (standing_errors_discipline / (shots_per_instance / 2) * 100)

                # Adjust hit rates to be mostly in the range of 70%-100%
                hit_rate_discipline = max(90, min(hit_rate_discipline, 100))
                hit_rate_prone_discipline = max(90, min(hit_rate_prone_discipline, 100))
                hit_rate_standing_discipline = max(90, min(hit_rate_standing_discipline, 100))

                discipline_details.append({
                    "Discipline": discipline,
                    "Instance": i + 1,
                    "Errors": {
                        "Prone": prone_errors_discipline,
                        "Standing": standing_errors_discipline
                    },
                    "Hit Rates": {
                        "Total": hit_rate_discipline,
                        "Prone": hit_rate_prone_discipline,
                        "Standing": hit_rate_standing_discipline
                    }
                })

            data.append({
                "Date": current_date.strftime("%Y-%m-%d"),
                "Mode": mode,
                "Trainings_mode": training_mode,
                "Wind Conditions": wind_condition,
                "Daily Summary": {
                    "Total Shots": total_shots,
                    "Prone Errors": prone_errors,
                    "Standing Errors": standing_errors,
                    "Overall Hit Rate": overall_hit_rate,
                    "Prone Hit Rate": prone_hit_rate,
                    "Standing Hit Rate": standing_hit_rate
                },
                "Discipline Details": discipline_details
            })

        current_date += timedelta(days=random.randint(1, 3))

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Beispiel für die Verwendung der Funktion
start_date = datetime(2024, 9, 1)
end_date = datetime(2024, 11, 30)
file_path = "JSON\biathlon_statistics_K_3_3.json"
generate_random_data(start_date, end_date, file_path)