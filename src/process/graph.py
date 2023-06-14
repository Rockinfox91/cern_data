import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import seaborn as sns
import scipy

from src.process.time_thing import get_date_first_data, get_date_last_data, get_unix_time_from_date
from src.process.data_analyse import lire_data


def get_graph_from_file(file: str, coly: [str], colx: str = "Time", name: str = None,
                        x_limit: [float] = [None, None], y_limit: [float] = [None, None],
                        ax_y_name: [str] = "Values", is_saving: bool = False, timing: str = "min",
                        put_y_line: int = None, y_line_name=None,
                        start_date: str = None, end_date: str = None,
                        other_coly: str = None, other_coly_name: str = "Values"):
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

    Returns:
        None
    """

    df = lire_data(file)

    x_limit_date = [start_date, end_date]

    # Check the type of coly
    if isinstance(coly, str):
        coly = [coly]

    # TODO Start x time after start or End y time before end

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
        else:
            raise Exception
    except Exception as e:
        print(e)
        print("Timing needs to be sec, min, hour, or day!")


    #TODO : Lacune donnée, tester le temps entre chaque donnée et si > 1h (exemple), ne pas afficher

    fig, ax = plt.subplots(figsize=(10, 6))

    # Get the current date
    current_date = datetime.datetime.now()

    # Extract year, month, and day as strings
    year = str(current_date.year)
    month = str(current_date.month).zfill(2)  # Zero-padding for single-digit months
    day = str(current_date.day).zfill(2)  # Zero-padding for single-digit days

    ax.text(0.99, 1.01, f"CERN Run\n{day}-{month}-{year}",
            transform=ax.transAxes, ha='right', fontweight='bold')

    # Get the metadata of the file
    file_first_data_date = get_date_first_data(file)
    file_first_data_datetime = file_first_data_date.strftime("%Y-%m-%d %H:%M:%S")
    file_last_data_date = get_date_last_data(file)
    file_last_data_datetime = file_last_data_date.strftime("%Y-%m-%d %H:%M:%S")

    # Display the file's creation date and time on the graph
    ax.text(-0.1, 1.13, f"File begins at: {file_first_data_datetime}",
            transform=ax.transAxes, ha='left', va='top')
    ax.text(-0.1, 1.1, f"File finishes at: {file_last_data_datetime}",
            transform=ax.transAxes, ha='left', va='top')

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
