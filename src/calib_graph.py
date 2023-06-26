import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from src.process.graph import scatter_hist, get_afternoon_tension_data

all_periods = [["2023.06.15_14:25:00","2023.06.15_17:37:00"],
              ["2023.06.16_13:35:00","2023.06.16_17:37:00"],
              ["2023.06.19_14:10:00", "2023.06.19_17:22:00"],
              ["2023.06.20_11:49:00", "2023.06.21_09:49:00"],
              ["2023.06.21_12:10:00", "2023.06.22_09:09:00"],
              ["2023.06.22_13:09:00", "2023.06.23_17:40:00"],
              ["2023.06.22_17:30:00", "2023.06.26_10:00:00"]]

if __name__ == "__main__":


    finaldata = get_afternoon_tension_data("linux_final_data",all_periods)

    #On retire les valeurs Not found, Cold Garage et Hot Garage
    finaldata = finaldata[(finaldata["Position"] == 'A') | (finaldata["Position"] == 'B') |
                          (finaldata["Position"] == 'C') | (finaldata["Position"] == 'D')]

    finaldata = finaldata[finaldata["time"]<50000]
    scatter_hist(finaldata)