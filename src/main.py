import numpy as np
import pandas as pd
from src.process.graph import get_easy_time_graph


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

    # Soustraire la première valeur de la colonne "time" pour que le temps commence à 0
    df['time'] = df['time'] - df['time'].iloc[0]

    return df


if __name__ == "__main__":
    print("----- Début programme -----")
    data = lire_data("cern_data_run10")
    print(data)

    print("Graphe simple de Ta en fonction du temps")
    get_easy_time_graph(data, ["Ta", "Tb", "Tc", "Td"])
    get_easy_time_graph(data, ["Hin", "Hout", "Hamb", "CryoL"])
    get_easy_time_graph(data, ["Tamb", "Tout", "flowIn"])
    get_easy_time_graph(data, ["I1", "I3"])
