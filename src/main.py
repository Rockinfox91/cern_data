import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def lire_data(data_file_name):
    # Chemin vers le fichier de données
    chemin_fichier = f'data/{data_file_name}.txt'
    print(f"Lecture du fichier \"{chemin_fichier}\"")

    # Lire le fichier de données
    donnees = np.genfromtxt(chemin_fichier, delimiter='\t')

    # Étiquettes des colonnes
    etiquettes = ['time', 'flowIn', 'Tout', 'Hout', 'Tamb', 'Hamb', 'Hin', 'CryoL', 'Ta', 'Tb', 'Tc', 'Td', 'I1', 'I3']

    # Créer un DataFrame pandas avec les données et les étiquettes
    df = pd.DataFrame(donnees, columns=etiquettes)
    print("Data frame créé.")

    return df


def get_easy_graph(df, colx, coly):
    if isinstance(coly, str):
        coly = [coly]

    num_plots = len(coly)
    fig, axes = plt.subplots(2, 2, figsize=(10, 10), squeeze=False)
    axes = axes.flatten()

    for i in range(num_plots):
        ax = axes[i]
        ax.plot(df[colx], df[coly[i]])
        ax.set_xlabel(colx)
        ax.set_ylabel(coly[i])

    if num_plots == 1:
        fig.suptitle(f"Graphe de {coly[0]} par rapport à {colx}")
    else:
        fig.suptitle("Graphique des températures des points\nA, B, C et D en fonction du temps")
        for i, col in enumerate(coly):
            axes[i].set_title(col)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    print("----- Début programme -----")
    data = lire_data("cern_data_run10")
    print(data)

    print("Graphe simple de Ta en fonction du temps")
    get_easy_graph(data, "time", ["Ta","Tb","Tc","Td"])