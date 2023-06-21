from src.process.data_analyse import lire_data
from src.process.graph import plot_data_with_dct
from src.process.time_thing import merge_dataframes_by_unix
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

if __name__=="__main__":

    data_win = lire_data("windows_final_data")
    data_lin = lire_data("linux_final_data")
    data = merge_dataframes_by_unix(data_win,data_lin)

    #To get seconds in time unit
    data["UnixTimestamp"] = data["UnixTimestamp"] - data["UnixTimestamp"].iloc[0]

    plt.plot(data["UnixTimestamp"], data["Tension4"], "r-", label="Tension4")
    plt.plot(data["UnixTimestamp"], data["Tamb"], "b-", label="Tamb")
    plt.legend()
    plt.show()

    #to select the period
    data = data[((data["UnixTimestamp"] > 443500) & (data["UnixTimestamp"] < 508600))
                |((data["UnixTimestamp"] > 543500) & (data["UnixTimestamp"] < 595900))
                | ((data["UnixTimestamp"] > 721600) & (data["UnixTimestamp"] < 779800))
                | ((data["UnixTimestamp"] > 27100) & (data["UnixTimestamp"] < 55900))
                ]

    print(data)

    plt.plot(data["UnixTimestamp"],data["Tension4"],"r-",label="Tension4")
    plt.plot(data["UnixTimestamp"], data["Tamb"], "b-", label="Tamb")
    plt.legend()
    plt.show()

    #SCATTER PLOT

    temperature = data["Tamb"].to_numpy()
    tension = data["Tension4"].to_numpy()

    # Calculate the density of points at each location
    heatmap, xedges, yedges = np.histogram2d(temperature, tension, bins=10)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    # Create scatter plot with color-mapped points
    plt.imshow(heatmap.T, extent=extent, origin='lower', aspect='auto', cmap='hot')
    plt.colorbar(label='Density')
    plt.scatter(temperature, tension, c='white', edgecolors='black')

    # Add the linear fit line
    fit_coeffs = np.polyfit(temperature, tension, deg=1)
    fit_x = np.linspace(min(temperature), max(temperature), 100)
    fit_y = np.polyval(fit_coeffs, fit_x)
    plt.plot(fit_x, fit_y, color='blue', label='Linear Fit')

    plt.xlabel('Temperature')
    plt.ylabel('Tension')
    plt.title('Density Scatter Plot')
    plt.show()


    # Utilisation de la fonction plot_data_with_dct
    plot_data_with_dct(data, x='UnixTimestamp', y='Tamb', max_freq=2)

