import sys
import argparse

from src.process.data_analyse import append_data

if __name__ == "__main__":

    if len(sys.argv) > 1:
        # Create the argument parser
        parser = argparse.ArgumentParser(description="Generate a file from all file data given.")

        # Add the arguments to the parser
        parser.add_argument("file1", type=str, help="The path to the file1 containing the data (with extension).")
        parser.add_argument("file2", type=str, help="The path to the file2 containing the data (with extension).")
        parser.add_argument("sort_col", type=str, help="The column to sort the data by.")
        parser.add_argument("name", type=str, help="The name of the final file.")

        # Parse the command-line arguments
        args = parser.parse_args()

        # Call your function with the parsed arguments
        append_data(args.file1, args.file2, args.name, args.sort_col)
