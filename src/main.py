from process.graph import get_easy_graph
from process.data_analyse import *

if __name__ == "__main__":
    print("----- Début programme -----")

    print(get_date_first_data("copy_cern_data_run23"))
    print(get_date_last_data("copy_cern_data_run23"))
    get_easy_graph("copy_cern_data_run23",["Hin","Hout"],is_saving=True)

    print("----- Fin programme -----")
