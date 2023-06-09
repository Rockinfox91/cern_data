from process.graph import get_easy_graph
from process.data_analyse import *

if __name__ == "__main__":
    print("----- Début programme -----")

    print(get_time_from_secondstep(1000 * 60, get_date_first_data("copy_cern_data_run29")))
    get_easy_graph("copy_cern_data_run29", ["T_bottom","T_elbow","T_intermediate","T_top"],
                   x_limit=[1.5,9]
                   ,y_limit=[-195,-148], ax_y_name="Temperatures (°C)" ,timing="hours", ax_x_name = "Time from start (hours)", is_saving=True, name="Temperature_differences")
    print(get_time_from_secondstep(15*3600, get_date_first_data("copy_cern_data_run29")))
    print("----- Fin programme -----")
