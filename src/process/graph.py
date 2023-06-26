import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
import seaborn as sns
from scipy.fftpack import idct

from src.process.time_thing import get_date_first_data, get_date_last_data, get_unix_time_from_date
from src.process.data_analyse import lire_data, calculate_dct


def get_graph_from_file(file: str, coly: [str], colx: str = "Time", name: str = None,
                        x_limit: [float] = [None, None], y_limit: [float] = [None, None],
                        ax_y_name: [str] = "Values", is_saving: bool = False, timing: str = "min",
                        put_y_line: int = None, y_line_name=None,
                        start_date: str = None, end_date: str = None,
                        other_coly: str = None, other_coly_name: str = "Values", df_given: bool=False):
    """
    Generate a graph from data in a file.

    Parameters:
        - file (str): The path to the file containing the data.
        - coly (str or list[str]): The column(s) to plot on the y-axis.
        - colx (str, optional): The column to plot on the x-axis. Defaults to "Time".
        - name (str, optional): The name of the graph. Defaults to None.
        - x_limit (list[float], optional): The lower and upper limits of the x-axis. Defaults to [None, None].
        - y_limit (list[float], optional): The lower and upper limits of the y-axis. Defaults to [None, None].
        - ax_y_name (str, optional): The label for the y-axis. Defaults to "Values".
        - is_saving (bool, optional): Whether to save the plot as an image. Defaults to False.
        - timing (str, optional): The timing unit for the x-axis. Can be "sec", "min", or "hour". Defaults to "min".
        - put_y_line (int, optional): The y-coordinate of a horizontal line to add to the plot. Defaults to None.
        - y_line_name (str, optional): The label for the y-line. Defaults to None.
        - start_date (str, optional): The start date for the x-axis. Defaults to None.
        - end_date (str, optional): The end date for the x-axis. Defaults to None.
        - other_coly (str, optional): The column to plot on the second y-axis. Defaults to None.
        - other_coly_name (str, optional): The label for the second y-axis. Defaults to "Values".
        - df (bool, optional): if file is a df.
    Returns:
        None
    """

    if not isinstance(file, pd.DataFrame):
        df = lire_data(file)
    else:
        df = file

    x_limit_date = [start_date, end_date]

    # Check the type of coly
    if isinstance(coly, str):
        coly = [coly]

    if x_limit_date[0]:
        x_limit[0] = get_unix_time_from_date(x_limit_date[0]) - df[colx].iloc[0]
    if x_limit_date[1]:
        x_limit[1] = get_unix_time_from_date(x_limit_date[1]) - df[colx].iloc[0]

    if x_limit[0] is None:
        x_limit[0] = 0
    if x_limit[1] is None:
        x_limit[1] = df[colx].max() - df[colx].iloc[0]

    print(x_limit)

    try:
        # Format x-axis based on timing parameter
        if timing == "sec":
            df[colx] = (df[colx] - df[colx].iloc[0])
        elif timing == "min":
            df[colx] = (df[colx] - df[colx].iloc[0]) / 60
            x_limit[0] = x_limit[0] / 60
            x_limit[1] = x_limit[1] / 60
        elif timing == "hour":
            df[colx] = (df[colx] - df[colx].iloc[0]) / 3600
            x_limit[0] = x_limit[0] / 3600
            x_limit[1] = x_limit[1] / 3600
        elif timing == "day":
            df[colx] = (df[colx] - df[colx].iloc[0]) / 86400
            x_limit[0] = x_limit[0] / 86400
            x_limit[1] = x_limit[1] / 86400
            # TODO: Si days, afficher les jours en date.
        else:
            raise Exception
    except Exception as e:
        print(e)
        print("Timing needs to be sec, min, hour, or day!")

    # TODO : affichage data à partir de start_date = t0.

    fig, ax = plt.subplots(figsize=(10, 6))

    # Get the current date
    current_date = datetime.now()

    # Extract year, month, and day as strings
    year = str(current_date.year)
    month = str(current_date.month).zfill(2)  # Zero-padding for single-digit months
    day = str(current_date.day).zfill(2)  # Zero-padding for single-digit days

    ax.text(0.99, 1.01, f"CERN Run\n{day}-{month}-{year}",
            transform=ax.transAxes, ha='right', fontweight='bold')

    if not isinstance(file, pd.DataFrame):
        # Get the metadata of the file
        file_first_data_date = get_date_first_data(file)
        file_first_data_datetime = file_first_data_date.strftime("%Y-%m-%d %H:%M:%S")
        file_last_data_date = get_date_last_data(file)
        file_last_data_datetime = file_last_data_date.strftime("%Y-%m-%d %H:%M:%S")

        # Display the file's creation date and time on the graph
        ax.text(-0.1, 1.13, f"Data file begins at: {file_first_data_datetime}",
                transform=ax.transAxes, ha='left', va='top')
        ax.text(-0.1, 1.1, f"Data file finishes at: {file_last_data_datetime}",
                transform=ax.transAxes, ha='left', va='top')

    # TODO: ajouter Graph begins at ... end at ...

    # Plot each column from coly on the first y-axis
    color_palette = plt.rcParams['axes.prop_cycle'].by_key()['color']
    for i, col in enumerate(coly):
        ax.plot(df[colx], df[col], label=col, color=color_palette[i % len(color_palette)])

    # Plot the other_coly on the second y-axis
    if other_coly:
        color_palette2 = plt.cm.Set2(np.linspace(0, 1, len(other_coly)))  # Generate a color palette for other_coly
        ax2 = ax.twinx()  # Create a twin y-axis
        for i, coly2 in enumerate(other_coly):
            ax2.plot(df[colx], df[coly2], label=coly2, color=color_palette2[i])
        ax2.set_ylabel(other_coly_name)  # Set the label for the second y-axis

    if put_y_line:
        # Add a horizontal line at y=put_y_line
        ax.axhline(y=put_y_line, linestyle='--', color='red')
        ax.text(0.93, 0.21, y_line_name,
                transform=ax.transAxes, ha='right', fontweight='bold')

    # Set axis labels and title
    if colx == "Time" or colx == "LinuxTime":
        ax.set_xlabel(f"Time since beginning ({timing})")
    else:
        ax.set_xlabel(colx)
    ax.set_ylabel(ax_y_name)

    # Define default values for start_time and end_time if not specified
    ax.set_xlim(x_limit[0], x_limit[1])

    # Set y-axis limit if provided
    if y_limit is not None:
        ax.set_ylim(y_limit)

    # Format x-axis ticks if timing is set to "date"
    if timing == "date":
        ax.set_xticklabels(df[colx], rotation=45)

    # Add title
    ax.set_title(f"{name}_{file}")

    # Add legend
    if other_coly:
        ax2.legend(loc='center left', bbox_to_anchor=(1.13, 0.5))
    ax.legend(loc='center right', bbox_to_anchor=(-0.13, 0.5))

    fig.tight_layout()

    # Save the plot if is_saving is True
    if is_saving and name:
        plt.savefig(f"img/cold_test/plot_{name}.png", dpi=300)

    # Show the plot
    plt.show()


def plot_correlation_matrix(df: pd.DataFrame, exclude_columns: [str] = None,
                            title: str = None,
                            ):
    """
    Plot a correlation matrix heatmap.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing the data.
        exclude_columns ([str], optional): The list of column names to exclude. Defaults to None.
        title (str, optional): Title for the graph. Default to None.

    Raises:
        ValueError: If the DataFrame does not contain any numeric columns after excluding the specified columns.

    Returns:
        None
    """

    if exclude_columns:
        # Filter out the columns to exclude
        df = df.drop(columns=exclude_columns, errors='ignore')

    # Select columns that contain numeric values
    numeric_columns = df.select_dtypes(include=np.number).columns

    if len(numeric_columns) == 0:
        raise ValueError("The DataFrame does not contain any numeric columns.")

    # Subset the DataFrame based on columns with numeric values
    df = df[numeric_columns].iloc[:, 1:]

    # Compute the correlation matrix
    corr_matrix = np.corrcoef(df.values.T)

    # Check if the correlation matrix is symmetric
    is_symmetric = np.allclose(corr_matrix, corr_matrix.T)

    # Create a figure and axis for the heatmap
    fig, ax = plt.subplots(figsize=(8, 6), dpi=100)  # Adjust the values as needed

    # Draw the heatmap
    if is_symmetric:
        print("Matrix is a triangle because of symmetry")
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, annot=True, fmt=".1f", vmin=-1, vmax=1, center=0, cmap="seismic", mask=mask, ax=ax)
    else:
        sns.heatmap(corr_matrix, annot=True, fmt=".1f", vmin=-1, vmax=1, center=0, cmap="seismic", ax=ax)

    # Get the column names from the DataFrame
    column_names = df.columns

    # Set the x and y labels using the column names
    ax.set_xticklabels(column_names, rotation=90)
    ax.set_yticklabels(column_names, rotation=0)

    if title:
        # Add title
        ax.set_title(f"{title}")

    # Adjust the margins
    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.2)

    # Show the plot
    plt.show()


def scatter_hist(df):
    """
        Generate a scatter histogram plot based on the provided DataFrame.

        Parameters:
        - df (pandas.DataFrame): The input DataFrame containing the necessary data columns.

        Returns:
        None

        This function generates a scatter histogram plot using the specified DataFrame. The plot includes:
        - Joint scatter plot with custom colors defined by the 'Category' column
        - Mean and standard deviation values displayed for each 'Puller' group
        - Logarithmic x-axis scale
        - Dashed lines representing different time constants
        - Legend for the type of points
        - Customized figure size and margins

        The DataFrame is expected to have the following columns:
        - 'Puller': Categorical column representing different groups or categories
        - 'Position': Categorical column representing different positions
        - 'time': Numeric column representing the time on position (in minutes)
        - 'TensionMax': Numeric column representing the maximum tension (in Newtons) 10 seconds after movement

        Example usage:
        >>> scatter_hist(data_df)

        Note:
        - This function requires the 'seaborn' and 'matplotlib' libraries.
    """
    # Définir les nuances de rouge et de bleu
    red_palette = sns.color_palette("Reds", 1)
    blue_palette = sns.color_palette("Blues", 1)

    # Combiner les palettes de couleurs
    custom_palette = blue_palette + red_palette

    # Combinaison des paramètres "Puller" et "Position" en une seule variable
    df["Category"] = df["Puller"] + " - " + df["Position"]

    # Trier la colonne 'Category' par ordre alphabétique
    df_sorted = df.sort_values('Position',ascending=False)

    # Créer le histogramme joint avec les couleurs définies par "Category" et la palette personnalisée
    jointplot = sns.jointplot(data=df_sorted, x="time", y="TensionMax", hue="Puller", markers=["o", "s", "^", '*'],
                              palette=custom_palette, style=df_sorted["Position"], ylim=(7, 32))
    # TODO Symbole à la place de la palette de couleur

    # Obtenir valeur moyenne et répartition de distribution
    mean = {}
    std = {}
    for pull, group in df.groupby('Puller'):
        mean[pull] = group["TensionMax"].mean()
        std[pull] = group["TensionMax"].std()

    # Changer le nom de l'axe des abscisses (x-axis)
    jointplot.ax_joint.set_xlabel("Time on position (min)")

    # Retirer distribution x
    jointplot.ax_marg_x.remove()

    # Changer le nom de l'axe des ordonnées (y-axis)
    jointplot.ax_joint.set_ylabel("Max Tension 10s after moved (N)")

    # Axe des x en logarithmique
    plt.xscale('log')

    # Ajouter les lignes en pointillés pour les constantes temporelles
    time_constants = [1, 10, 30, 60, 120,1000,3800]  # Valeurs des constantes temporelles à représenter
    time_constants_name = ["1min", "10min", "30min", "1h", "2h","1 Night","Weekend"]

    # Get the axes of the jointplot
    ax_joint = jointplot.ax_joint

    #Ajout des différentes lignes

    plt.axhline(y=mean["DS2"], linestyle="--", color="blue", linewidth=0.2)
    # Ajout du texte aux coordonnées spécifiées
    ax_joint.annotate(r"$\mu_{DS2}$ = "+f"{round(mean['DS2'],2)}N", xy=(250, mean["DS2"]+0.2), xycoords='data', ha='left',
                      va='bottom', fontsize=10, color="blue")
    ax_joint.annotate(r"$\sigma_{DS2}$ = " + f"{round(std['DS2'], 2)}N", xy=(250, mean["DS2"]-0.3), xycoords='data', ha='left',
                      va='top', fontsize=10, color="blue")
    plt.axhline(y=mean["DS4"], linestyle="--", color="red", linewidth=0.2)
    # Ajout du texte aux coordonnées spécifiées
    ax_joint.annotate(r"$\mu_{DS4}$ = "+f"{round(mean['DS4'],2)}N", xy=(250, mean["DS4"]+0.2), xycoords='data', ha='left',
                      va='bottom', fontsize=10, color="red")
    ax_joint.annotate(r"$\sigma_{DS4}$ = " + f"{round(std['DS4'], 2)}N", xy=(250, mean["DS4"]-0.3), xycoords='data',
                      ha='left', va='top', fontsize=10, color="red")

    for i in range(len(time_constants)):
        # Ajouter une ligne en pointillés
        plt.axvline(x=time_constants[i], linestyle="--", color="gray", linewidth=0.2)
        # Ajout du texte aux coordonnées spécifiées
        ax_joint.annotate(time_constants_name[i], xy=(time_constants[i], 30), xycoords='data', ha='left',
                          va='center', fontsize=10, color="gray")

    # Customize the legend
    legend = ax_joint.legend(title='Type of points')
    # Position the legend outside the plot
    legend.set_bbox_to_anchor((-0.2, 1))  # Adjust the values as needed
    # Set the properties of the legend box
    legend.get_frame().set_linewidth(2)  # Border width

    jointplot.ax_marg_x.set_aspect(2)  # Adjust the aspect ratio as needed
    # Resize the figure or adjust subplot ratios
    jointplot.fig.set_size_inches(10, 6)  # Adjust the values as needed
    # Adjust the figure margins
    jointplot.fig.tight_layout()

    plt.show()


def get_afternoon_tension_data(file: str, time: [[str]]):
    """
       Extract tension data for the afternoon periods specified in the given file.

       Parameters:
       - file (str): The path to the file containing the data.
       - time (list of lists): The list of time periods in the format [[start_time1, end_time1], [start_time2, end_time2], ...],
                               where start_time and end_time are strings representing timestamps in the format "%Y.%m.%d_%H:%M:%S".

       Returns:
       pandas.DataFrame: The final DataFrame containing the extracted tension data for the specified afternoon periods.

       This function reads data from the specified file and extracts tension data for the afternoon periods defined by the 'time' parameter.
       It creates a new DataFrame with columns 'TensionMax', 'time', 'Puller', and 'Position' to store the extracted data.
       The function performs the following steps for each afternoon period:
       - Converts the start and end times to datetime objects.
       - Retrieves data within the specified time range.
       - Processes the data to identify movement events and calculate relevant values.
       - Appends the extracted tension data to the final DataFrame.

       Example usage:
       >>> afternoon_data = get_afternoon_tension_data('datafile', [['2023.06.23_13:00:00', '2023.06.23_17:00:00'], ['2023.06.24_14:30:00', '2023.06.24_16:30:00']])

       Note:
       - This function requires the 'pandas' library.
       - The input file is expected to contain the necessary columns: 'LinuxTime', 'Length2', 'TargetLength2', 'Tension2', and 'Tension4'.
    """
    all_data = lire_data(file)
    final_df = pd.DataFrame(columns=['TensionMax', 'time', 'Puller', 'Position'])
    date_format = "%Y.%m.%d_%H:%M:%S"
    total_i = 0
    for period in time:
        start_time = period[0]
        end_time = period[1]
        # Convertir la chaîne de caractères en objet datetime
        start_date_obj = datetime.strptime(start_time, date_format)
        end_date_obj = datetime.strptime(end_time, date_format)

        # Obtenir le timestamp Unix
        start_unix = start_date_obj.timestamp()
        end_unix = end_date_obj.timestamp()

        boundary_data = all_data[(all_data["LinuxTime"] > start_unix) & (all_data["LinuxTime"] < end_unix)]

        i = 0
        unixtime_from_start_move = 0
        unixtime_from_end_move = 0
        # Créer un DataFrame vide
        df = pd.DataFrame(columns=['TensionMax', 'time', 'Puller', 'Position'])
        for index, row in boundary_data.iterrows():
            actual_length = row['Length2']
            target_length = row['TargetLength2']
            unixtime = row['LinuxTime']

            # Récupère le moment où la source bouge
            if target_length != 0 and all_data["TargetLength2"].iloc[index - 1] == 0:
                puller = "DS4" if (actual_length < target_length) else "DS2"
                i += 1

                unixtime_from_start_move = unixtime
                time_position_stayed_here = unixtime - unixtime_from_end_move
                # Ajouter une nouvelle ligne
                sensibility = 5
                if (actual_length < 577 + sensibility) and (actual_length > 577 - sensibility):
                    position = "D"
                elif (actual_length < 557 + sensibility) and (actual_length > 557 - sensibility):
                    position = "C"
                elif (actual_length < 516 + sensibility) and (actual_length > 516 - sensibility):
                    position = "B"
                elif (actual_length < 453 + sensibility) and (actual_length > 453 - sensibility):
                    position = "A"
                elif (actual_length < 585 + sensibility) and (actual_length > 585 - sensibility):
                    position = "Cold_Garage"
                elif (actual_length < 605 + sensibility) and (actual_length > 605 - sensibility):
                    position = "Hot_Garage"
                elif actual_length > 585:
                    position = "Unknown_Garage"
                else:
                    position = "Not found"

                nouvelle_ligne = {"TensionMax": row["Tension4"], "Puller": puller, "Position": position,
                                  'time': int(time_position_stayed_here / 60)}
                df = pd.concat([df, pd.DataFrame(nouvelle_ligne, index=[0])], ignore_index=True)

            # Récupère le moment où la source a fini de bouger
            if target_length == 0 and all_data["TargetLength2"].iloc[index - 1] != 0:
                unixtime_from_end_move = unixtime

            # Récupérer tension max dans les 10 secondes après mouvement
            if (unixtime <= unixtime_from_start_move + 10):
                tension2_value = row["Tension2"]
                tension4_value = row["Tension4"]
                if puller == "DS2" and tension2_value > df["TensionMax"].iloc[-1]:
                    df.loc[df.index[-1], 'TensionMax'] = tension2_value
                if puller == "DS4" and tension4_value > df["TensionMax"].iloc[-1]:
                    df.loc[df.index[-1], 'TensionMax'] = tension4_value

        print(f"{i} data found.")
        total_i += i
        # Utilisez la fonction concat pour les concaténer
        final_df = pd.concat([final_df, df])
    print(df)
    print(f"Total data found : {total_i}")
    return final_df

