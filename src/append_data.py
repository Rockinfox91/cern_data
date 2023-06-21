import sys
import argparse

from src.process.data_analyse import append_all_data

if __name__ == "__main__":

    if len(sys.argv) > 1:
        # Create the argument parser
        parser = argparse.ArgumentParser(description="Generate a file from all file data given.")

        # Add the arguments to the parser
        parser.add_argument("file1", type=str, help="The path to the file1 containing the data. This file will be "
                                                    "added to another one (file2) or will be the exemple for all others"
                                                    " file taken (-a).")
        parser.add_argument("sort_col", type=str, help="The column to sort the data by.")
        parser.add_argument("finalname", type=str, help="The name of the final file.")
        parser.add_argument("--file2", type=str, help="The path to the file2 containing the data to add to file1.")
        parser.add_argument("--all-files","-a", action="store_true",
                            help="If you want all files like file1 to be concatenated together.")

        # Parse the command-line arguments
        args = parser.parse_args()

        # Call your function with the parsed arguments
        append_all_data(args.file1, args.finalname, args.sort_col, args.all_files, args.file2)

        # To get all linux files appended:
        # python -m src.append_data "RecordMonitoring" "LinuxTime" "linux_final_data" -a

        # To get all windows files appended:
        # python -m src.append_data "copy_cern" "Time" "windows_final_data" -a
