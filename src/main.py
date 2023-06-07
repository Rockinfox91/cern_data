from process.graph import get_easy_graph
from process.data_analyse import *

if __name__ == "__main__":
    print("----- Début programme -----")

    get_easy_graph("cern_data_run13", ["Hin", "Hout", "Hamb"], name="humidity_levels", ax_y_name="Humidity (%)",
                   start_time=55000)
    get_easy_graph("cern_data_run14", ["Hin", "Hout", "Hamb"], name="humidity_levels", ax_y_name="Humidity (%)")
    get_easy_graph("cern_data_run22", ["Hin", "Hout", "Hamb"], name="humidity_levels", ax_y_name="Humidity (%)")
    print(get_secondstep_from_time("2023-06-07 13:53:00", get_creation_date_of_file("cern_data_run22")))
    print(get_minutestep_from_time("2023-06-07 13:53:00", get_creation_date_of_file("cern_data_run22")))
    print(get_time_from_secondstep(3598, get_creation_date_of_file("cern_data_run22")))

    print("----- Fin programme -----")
