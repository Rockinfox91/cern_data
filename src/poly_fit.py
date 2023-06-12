import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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


if __name__ == "__main__":
    print("----- Début programme -----")
    data = lire_data("copy_cern_data_run29")

    fig, ax = plt.subplots(5)

    temps = ["Ta", "Tb", "Tc", "Td", "Tamb"]
    

    # polynomial approximation

    poly = []
    poly_T = []

    print(data)

    for temp in range(len(temps)):
        poly.append(np.polyfit(data["time"],data[temps[temp]],10))
        poly_T.append(np.poly1d(poly[temp])(data["time"]))

        ax[temp].plot(data["time"],data[temps[temp]])
        ax[temp].plot(data["time"],poly_T[temp])
        ax[temp].set_title(temps[temp])

    

    plt.show()
