import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import timedelta
import os


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


def get_easy_graph(file, coly, colx="time", name=None,
                   start_time=None, end_time=None, separate_plots=False, ax_y_name="Values"):
    df = lire_data(file)
    print("Fichier lu pour le graphique : ")
    print(df)

    if isinstance(coly, str):
        coly = [coly]

    if start_time is None:
        start_time = 0
    if end_time is None:
        end_time = df['time'].max()

    df_filtered = df.loc[(df['time'] >= start_time) & (df['time'] <= end_time)]

    fig, ax = plt.subplots(figsize=(8, 6))

    for i, col in enumerate(coly):
        ax.plot(df_filtered[colx], df_filtered[col], label=col)

    ax.set_xlabel(colx)
    ax.set_ylabel(ax_y_name)
    ax.set_title(f"{name}_{file}")
    ax.legend()

    # Récupérer les métadonnées du fichier
    file_creation_time = os.path.getctime(f"data/{file}.txt")
    file_creation_datetime = pd.to_datetime(file_creation_time, unit='s')
    file_creation_datetime += timedelta(hours=2)
    file_creation_datetime = file_creation_datetime.strftime("%Y-%m-%d %H:%M:%S")

    # Afficher la date et l'heure de création sur le graphe
    ax.text(-0.1, 1.1, f"Date : {file_creation_datetime}",
            transform=ax.transAxes, ha='left', va='top')

    if separate_plots:
        for i, col in enumerate(coly):
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.plot(df_filtered[colx], df_filtered[col])
            ax.set_xlabel(colx)
            ax.set_ylabel(ax_y_name)
            ax.set_title(f"{name}_{file}")
    plt.tight_layout()
    filename = f"plot_{file}_{name}"
    if start_time:
        filename += f"_from_{int(start_time)}"
    if start_time:
        filename += f"_to_{int(end_time)}"
    print(filename)
    plt.savefig(f"img/hot_test/{filename}", dpi=500)
    plt.show()
