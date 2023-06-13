import argparse
import sys

import pandas as pd

from src.process.graph import plot_correlation_matrix
from src.process.data_analyse import lire_data
from src.process.time_thing import merge_dataframes_by_unix


if __name__ == "__main__":

    if len(sys.argv) > 1:
        # Create an ArgumentParser object
        parser = argparse.ArgumentParser(description="Plot correlation matrix for data files.")

        # Add an argument to accept one or more file names
        parser.add_argument("files", nargs="+", help="Data file names")
        parser.add_argument("--merge", "-m", action="store_true", help="To merge two set of data together. Needs to be Windows then linux.")
        parser.add_argument("--exclude-columns", "-ec", nargs="+", help="Precise which column to exclude inside the final graph.", type=str)
        parser.add_argument("--title", "-t", nargs="+", type=str, help="To provide a title to the graph.", default=None)

        # Parse the command-line arguments
        args = parser.parse_args()

        # Iterate over the file names provided
        for i, file_name in range(len(args.files)), args.files:
            data_read = lire_data(file_name)
            plot_correlation_matrix(data_read, exclude_columns=args.exclude_columns, title=title)

        if args.merge:
            data_merged = merge_dataframes_by_unix(lire_data(args.files[0]), lire_data(args.files[1]))
            plot_correlation_matrix(data_merged, exclude_columns=args.exclude_columns, title=args.title)

    # To get a correlation graph of both Windows and Linux datas :
    # python -m src.correlation "copy_cern_data_run29.txt" "RecordMonitoring_2023.06.11_14-59-26.txt" -m -ec "CryoL" "FlowIn" "Hin"

    else:

        print("do \"python -m src.correlation -h\"")
