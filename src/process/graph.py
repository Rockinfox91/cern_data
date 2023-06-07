import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from .data_analyse import get_creation_date_of_file


def lire_data(data_file_name: str) -> pd.DataFrame:
    """
    Lire les données à partir d'un fichier texte.

    Parameters:
        data_file_name (str): Le nom du fichier de données à lire.

    Returns:
        pandas.DataFrame: Un DataFrame contenant les données lues à partir du fichier.

    Raises:
        IOError: Si le fichier spécifié n'existe pas.

    """
    # Chemin vers le fichier de données
    chemin_fichier = f'data/{data_file_name}.txt'
    print(f"Lecture du fichier \"{chemin_fichier}\"")

    # Lire le fichier de données
    donnees = np.genfromtxt(chemin_fichier,
                            delimiter='\t', dtype=[('time', 'float'),
                                                   ('flowIn', 'float'), ('Tout', 'float'),
                                                   ('Hout', 'float'), ('Tamb', 'float'), ('Hamb', 'float'),
                                                   ('Hin', 'float'), ('CryoL', 'float'), ('Ta', 'float'),
                                                   ('Tb', 'float'), ('Tc', 'float'), ('Td', 'float'),
                                                   ('I1', 'float'), ('I3', 'float')], skip_header=1)

    # Étiquettes des colonnes
    etiquettes = ['time', 'flowIn', 'Tout', 'Hout', 'Tamb', 'Hamb', 'Hin', 'CryoL', 'Ta', 'Tb', 'Tc', 'Td', 'I1', 'I3']

    # Créer un DataFrame pandas avec les données et les étiquettes
    df = pd.DataFrame(donnees, columns=etiquettes)
    print("Data frame créé.")

    # Soustraire la première valeur de la colonne "time" pour que le temps commence à 0
    df['time'] = df['time'] - df['time'].iloc[0]

    return df


def get_easy_graph(file: str, coly: [str], colx: str = "time", name: str = None,
                   start_time: int = None, end_time: int = None, separate_plots: bool = False, ax_y_name: str = "Values",
                   ax_x_name: str = "Time since beginning (min)"):
    """
        Génère un graphique simple à partir des données d'un fichier.

        Parameters:
            file (str): Le nom du fichier de données à utiliser.
            coly (str or list(str)): Le nom de la colonne ou une liste de noms de colonnes à afficher sur le graphique.
            colx (str, optional): Le nom de la colonne représentant l'axe des abscisses. Par défaut, "time".
            name (str, optional): Le nom à utiliser pour le graphique. Par défaut, None.
            start_time (float, optional): Le temps de début des données à afficher. Par défaut, 0.
            end_time (float, optional): Le temps de fin des données à afficher. Par défaut, le temps final.
            separate_plots (bool, optional): Indique si les courbes doivent être affichées séparément sur des graphiques distincts.
                Par défaut, False.
            ax_y_name (str, optional): Le nom de l'axe des ordonnées. Par défaut, "Values".
            ax_x_name (str, optional): Le nom de l'axe des abscisses. Par défaut, "Time since beginning (min)".

        Raises:
            IOError: Si le fichier spécifié n'existe pas.

        """
    # Lire les données du fichier
    df = lire_data(file)
    print("Fichier lu pour le graphique : ")
    print(df)

    # Vérifier le type de coly
    if isinstance(coly, str):
        coly = [coly]

    # Définir les valeurs par défaut pour start_time et end_time si elles ne sont pas spécifiées
    if start_time is None:
        start_time = 0
    if end_time is None:
        end_time = df['time'].max()

    # Filtrer les données en fonction des temps de début et de fin
    df_filtered = df.loc[(df['time'] >= start_time) & (df['time'] <= end_time)]

    # Créer la figure et les axes
    fig, ax = plt.subplots(figsize=(8, 6))

    # Tracer les courbes pour chaque colonne spécifiée dans coly
    for i, col in enumerate(coly):
        ax.plot(df_filtered[colx] / 60, df_filtered[col], label=col)

    # Définir les étiquettes des axes et le titre du graphique
    ax.set_xlabel(ax_x_name)
    ax.set_ylabel(ax_y_name)
    ax.set_title(f"{name}_{file}")
    ax.legend()

    # Récupérer les métadonnées du fichier
    file_creation_datetime = get_creation_date_of_file(file)
    file_creation_datetime = file_creation_datetime.strftime("%Y-%m-%d %H:%M:%S")

    # Afficher la date et l'heure de création sur le graphe
    ax.text(-0.1, 1.1, f"File begin at : {file_creation_datetime}",
            transform=ax.transAxes, ha='left', va='top')

    # Tracer les courbes séparément sur des graphiques distincts si l'option separate_plots est activée
    if separate_plots:
        for i, col in enumerate(coly):
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.plot(df_filtered[colx] / 60, df_filtered[col])
            ax.set_xlabel(ax_x_name)
            ax.set_ylabel(ax_y_name)
            ax.set_title(f"{name}_{file}")

    # Ajuster le placement des éléments dans le graphique
    plt.tight_layout()

    # Définir le nom du fichier de sauvegarde en fonction des paramètres spécifiés
    filename = f"plot_{file}_{name}"
    if start_time:
        filename += f"_from_{int(start_time)}"
    if start_time:
        filename += f"_to_{int(end_time)}"
    print(filename)

    # Sauvegarder le graphique en tant qu'image
    plt.savefig(f"img/hot_test/{filename}", dpi=100)
    plt.show()
