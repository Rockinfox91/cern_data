import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from correlation import correlation_matrix
from scipy.optimize import curve_fit

def lire_data(data_file_name):
    # Chemin vers le fichier de données
    chemin_fichier = f'data/{data_file_name}.txt'
    print(f"Lecture du fichier \"{chemin_fichier}\"")

    # Lire le fichier de données
    donnees = np.genfromtxt(chemin_fichier, delimiter='\t', dtype=[('time', 'float'), ('flowIn', 'float'), ('Tout', 'float'),
                                                                   ('Hout', 'float'), ('Tamb', 'float'), ('Hamb', 'float'),
                                                                   ('Hin', 'float'), ('CryoL', 'float'), ('Ta', 'float'),
                                                                   ('Tb', 'float'), ('Tc', 'float'), ('Td', 'float'),
                                                                   ('I1', 'float'), ('I3', 'float')],skip_header=1)

    # Étiquettes des colonnes
    etiquettes = ['time', 'flowIn', 'Tout', 'Hout', 'Tamb', 'Hamb', 'Hin', 'CryoL', 'Ta', 'Tb', 'Tc', 'Td', 'I1', 'I3']

    # Créer un DataFrame pandas avec les données et les étiquettes
    df = pd.DataFrame(donnees, columns=etiquettes)
    print("Data frame créé.")

    #enlever celles avant refroidissement
    df = df[df.time>(100000+df['time'].iloc[0])].reset_index(drop=True)

    # Soustraire la première valeur de la colonne "time" pour que le temps commence à 0
    df['time'] = df['time'] - df['time'].iloc[0]

    return df

def plot_temps(df, line, col):
    fig, ax = plt.subplots(len(col))

    for c in range(len(col)):
        ax[c].plot(df["time"],df[col[c]])
        ax[c].plot(df["time"],line[col[c]])
        ax[c].set_title(col[c])

    plt.show()
    

if __name__ == "__main__":
    print("----- Début programme -----")
    
    data = lire_data("copy_cern_data_run29")

    temps = ["Ta", "Tb", "Tc", "Td", "Tamb"]
    

    # polynomial approximation

    poly = []
    poly_T = pd.DataFrame()

    for temp in range(len(temps)):
        poly.append(np.polyfit(data["time"],data[temps[temp]],10))
        poly_T[temps[temp]]=np.poly1d(poly[temp])(data["time"])


    #data_matrix = correlation_matrix(poly_T)
    plot_temps(data, poly_T, temps)


