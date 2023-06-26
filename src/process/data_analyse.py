import numpy as np
import pandas as pd
import csv
import glob
import os
import scipy.optimize
from scipy.fftpack import dct


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

def lire_exel_data(file: str):
    # Specify the path to your Excel file
    file_path = f'data/{file}.xlsx'

    # Read the Excel file and create a DataFrame
    df = pd.read_excel(file_path)

    # Print the DataFrame
    print(df)

    return df

def get_all_files_like(start_name):
    file_names = glob.glob(os.path.join(f"data/{start_name}*"))
    txt_files = [file for file in file_names if file.endswith(".txt")]

    if not file_names:
        raise ValueError(f"No files found with the name starting by '{start_name}' in the directory.")

    if not txt_files:
        raise ValueError(f"No TXT files found with the name starting by '{start_name}' in the directory.")

    print(txt_files)
    return txt_files


def append_data(file1_name: str, file2_name: str, sort_column: str, name: str = None):
    """
    Appends the data from two files, sorts it based on a specified column, and writes the combined data to a new file.

    Args:
        file1_name (str): The name of the first file to read.
        file2_name (str): The name of the second file to read.
        sort_column (str): The column name to sort the combined data.
        name (str): The name of the output file.

    Returns:
        pd.DataFrame: The combined and sorted data as a pandas DataFrame.
    """

    # Read the content of the first file
    with open(f'{file1_name}', 'r') as file1:
        reader = csv.reader(file1, delimiter='\t')
        lines1 = list(reader)

    # Read the content of the second file
    with open(f'{file2_name}', 'r') as file2:
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

    print("Data combined...")

    if name:
        # Write the combined data to a new file
        combined_data.to_csv(f'data/{name}.txt', sep='\t', index=False)
        print(f"File {name}.txt written successfully.")

        print("Data written")

    return combined_data


def append_all_data(file1_name: str, name: str, sort_column: str, all_files: bool = False, file2_name: str = None):
    """
    Appends data from multiple files, sorts it based on a specified column, and writes the combined data to a new file.

    Args:
        file1_name (str): The name of the first file to read.
        name (str): The name of the output file.
        sort_column (str): The column name to sort the combined data.
        all_files (bool, optional): If True, reads all files that match the pattern of file1_name or file2_name. Defaults to False.
        file2_name (str, optional): The name of the second file to read. Required if all_files is False. Defaults to None.

    Returns:
        pd.DataFrame: The combined and sorted data as a pandas DataFrame.
    """

    if not all_files and not file2_name:
        raise SyntaxError("There is no file2 mentionned, or no -a option to take all data.")
    if all_files and file2_name:
        raise SyntaxError("You can't give file2, and the -a option at the same time (-h for help).")

    if all_files:
        # Read all files that looks like file1 and file2
        try:
            if file1_name[:6] == "Record":
                data = get_all_files_like("RecordMonitoring")
            elif file1_name[:4] == "copy":
                data = get_all_files_like("copy_cern_data_run")
            else:
                raise FileNotFoundError("File must start with Record or copy_data to be used.")
        except ValueError as e:
            print(e)
        except FileNotFoundError as e:
            print(e)
    else:
        # Read the content of all files and combining them
        combined_data = append_data(file1_name, file2_name, sort_column, name)
        return

    # Read the content of all files and combining them
    append_data(data[0], data[1], sort_column, name)
    for i in range(len(data) - 2):
        combined_data = append_data(f"data/{name}.txt", data[i + 2], sort_column, name)

    print(f"Final file {name}.txt written successfully.")

    return combined_data


def sin_func(x, a, omega, phase, b):
    return a * np.sin(omega * x + phase) + b


def get_curvefit(df: pd.DataFrame, columnx: str, columny: str
                 , function: callable, param0: [float], bounds: ([float], [float]) = (-np.inf, np.inf)
                 ,
                 ):
    x_data = df[columnx].to_numpy()
    y_data = df[columny].to_numpy()

    popt, pcov = scipy.optimize.curve_fit(function, x_data, y_data, p0=param0, bounds=bounds)
    perr = np.sqrt(np.diag(pcov))

    return popt, perr, pcov


def get_curvfit_sin(df, columnx: str, columny: str, param0: [float]):
    return get_curvefit(df, columnx, columny, sin_func, param0, bounds=(0, [np.inf, np.inf, 2 * np.pi, 40]))


def calculate_dct(data, y_name):
    """
    Calculate the Discrete Cosine Transform (DCT) coefficients.

    Args:
        data (pd.DataFrame): Input DataFrame containing the data.
        y (List[str]): List of column names representing the temperature data.

    Returns:
        List[np.ndarray]: List of DCT coefficients for each temperature column.
    """

    # Calculate the DCT for each temperature column
    y = data[y_name].values
    dct_result = dct(y, norm='ortho')
    return dct_result
