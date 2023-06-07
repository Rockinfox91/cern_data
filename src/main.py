from process.graph import get_easy_graph


if __name__ == "__main__":
    print("----- Début programme -----")

    get_easy_graph("cern_data_run13", ["Hin", "Hout", "Hamb"], name="humidity_levels", ax_y_name="Humidity (%)", start_time=55000)
    get_easy_graph("cern_data_run14",["Hin", "Hout", "Hamb"], name="humidity_levels", ax_y_name="Humidity (%)")