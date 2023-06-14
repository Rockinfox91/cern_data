import numpy as np
import pandas as pd
import csv


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
    print(f"Lecture du fichier \"{chemin_fichier}.txt\"")

    try:
        # Lecture du fichier en tant que DataFrame pandas
        df = pd.read_csv(chemin_fichier, sep='\t')
        print(df)
        return df

    except IOError:
        raise IOError(f"Le fichier {data_file_name}.txt n'existe pas.")


def append_data(file1_name: str, file2_name: str, name: str, sort_column: str):
    """
    Append data from file2 to file1, sort the combined data by 'Time', and save it to a new file.

    Parameters:
        file1_name (str): Name of the first file (without the file extension).
        file2_name (str): Name of the second file (without the file extension).
        name (str): Name of the final file.
        sort_column (str): The column on which sort the files.
    Returns:
        pd.DataFrame

    Raises:
        FileNotFoundError: If either file1 or file2 is not found in the 'data' directory.

    Examples:
        >>> append_data("file1", "file2", "file_combined")
    """

    #TODO : Take all files like file1 file2 and concatenate them. (parameter all bool)

    # Read the content of the first file
    with open(f'data/{file1_name}.txt', 'r') as file1:
        reader = csv.reader(file1, delimiter='\t')
        lines1 = list(reader)

    # Read the content of the second file
    with open(f'data/{file2_name}.txt', 'r') as file2:
        reader = csv.reader(file2, delimiter='\t')
        lines2 = list(reader)

    # Combine the lines from both files, excluding the first line from the second file
    combined_lines = lines1 + lines2[1:]

    # Create a DataFrame from the combined data
    combined_data = pd.DataFrame(combined_lines)

    # Extract column names from the first line of the first file
    column_names = combined_data.iloc[0, :]

    # Set the column names in the DataFrame
    combined_data.columns = column_names

    # Drop the first row (column names from the first file)
    combined_data = combined_data.iloc[1:, :]

    # Sort the combined data by the 'Time' column
    combined_data.sort_values(by=sort_column, inplace=True, ignore_index=True)

    # Write the combined data to a new file
    combined_data.to_csv(f'data/{name}.txt', sep='\t', index=False)
    print(f"File {name}.txt written successfully.")

    return combined_data
