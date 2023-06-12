import numpy as np
import pandas as pd

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
    chemin_fichier = f'data/{data_file_name}'
    print(f"Lecture du fichier \"{chemin_fichier}\"")

    try:
        # Lecture du fichier en tant que DataFrame pandas
        df = pd.read_csv(chemin_fichier, sep='\t')
        print(df)
        return df

    except IOError:
        raise IOError(f"Le fichier {data_file_name} n'existe pas.")
