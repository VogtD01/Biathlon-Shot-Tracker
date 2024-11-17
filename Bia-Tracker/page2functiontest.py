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

####################################

def main():
    st.title("Biathlon Statistics")

    file_path = os.path.join("JSON", "biathlon_statistics_K_DV_01.json")
    statistics = load_statistics(file_path)

    if statistics:
        total_shots = calculate_total_shots(statistics)
        total_prone_errors = calculate_prone_errors(statistics)
        total_standing_errors = calculate_standing_errors(statistics)

        #Sprint statistics
        #sprint_count, total_shots_sprint, total_prone_errors_sprint, total_standing_errors_sprint, sprint_hit_rate, sprint_hit_rate_prone, sprint_hit_rate_standing = analyze_discipline(file_path, "Sprint")

        #individual statistics
        #individual_count, total_shots_individual, total_prone_errors_individual, total_standing_errors_individual, individual_hit_rate, individual_hit_rate_prone, individual_hit_rate_standing = analyze_discipline(file_path, "Individual")

       
        # Individual statistics all
        #ind_all_c, ts_all_c, pe_all_c, se_all_c, hr_all_c, hrp_all_c, hrs_all_c = analyze_discipline(file_path, "Individual")

        # Individual statistics training
        #ind_tr_c, ts_tr_c, pe_tr_c, se_tr_c, hr_tr_c, hrp_tr_c, hrs_tr_c = analyze_discipline(file_path, "Individual", mode="Training")

        # Individual statistics competition
        #ind_comp_c, ts_comp_c, pe_comp_c, se_comp_c, hr_comp_c, hrp_comp_c, hrs_comp_c = analyze_discipline(file_path, "Individual", mode="Competition")

        # Show individual statistics all, komplex
       # ind_all_k_c, ts_all_k_c, pe_all_k_c, se_all_k_c, hr_all_k_c, hrp_all_k_c, hrs_all_k_c = analyze_discipline(file_path, "Individual", training_mode="Komplex")

        # Show individual statistics training, komplex 
        #ind_tr_k_c, ts_tr_k_c, pe_tr_k_c, se_tr_k_c, hr_tr_k_c, hrp_tr_k_c, hrs_tr_k_c = analyze_discipline(file_path, "Individual", mode="Training", training_mode="Komplex")

        # Show individual statistics training, TNS
        #ind_tr_tns_c, ts_tr_tns_c, pe_tr_tns_c, se_tr_tns_c, hr_tr_tns_c, hrp_tr_tns_c, hrs_tr_tns_c = analyze_discipline(file_path, "Individual", training_mode="TNS")
        #---------------------------------------
        
        hit_rates_over_time, hit_rate_prone_over_time, hit_rate_standing_over_time = collect_hit_rates(file_path, "Individual")

        show_prone_standing = st.checkbox("Show Prone/Standing Hit Rate", value=True)


        plot_hit_rates(hit_rates_over_time, hit_rate_prone_over_time, hit_rate_standing_over_time, show_prone_standing)

        # Compare disciplines
        discipline_stats = compare_disciplines(file_path)
        plot_discipline_comparison(discipline_stats)

        # Compare wind conditions globally across all disciplines
        wind_stats = compare_wind_conditions(file_path)
        
        plot_wind_condition_comparison(wind_stats)

        #---------------------------------
        #analyse individual
        ind_all_c, ts_all_c, pe_all_c, se_all_c, hr_all_c, hrp_all_c, hrs_all_c = analyze_discipline(file_path, "Individual")
        st.write("Individual statistics all")
        st.write(f"Count: {ind_all_c}")
        st.write(f"Total Shots: {ts_all_c}")

        hit_rates_over_time, hit_rate_prone_over_time, hit_rate_standing_over_time = collect_hit_rates(file_path, "Individual")
        st.write("hir rates over time")
        #st.write(hit_rates_over_time, hit_rate_prone_over_time, hit_rate_standing_over_time)

        #
        overall_hit_rates_over_time, prone_hit_rates_over_time, standing_hit_rates_over_time = collect_overall_hit_rates(file_path)
        show_prone_standing = st.checkbox("Show Prone/Standing Hit Rate2", value=True)
        plot_overall_hit_rates(overall_hit_rates_over_time, prone_hit_rates_over_time, standing_hit_rates_over_time, show_prone_standing)


        
