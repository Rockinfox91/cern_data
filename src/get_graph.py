import sys
import argparse

from src.process.graph import *
from src.process.time_thing import *

if __name__ == "__main__":

    if len(sys.argv) > 1:
        # Create the argument parser
        parser = argparse.ArgumentParser(description="Generate a graph from data in a file.")

        # Add the arguments to the parser
        parser.add_argument("file", type=str, help="The path to the file containing the data.")
        parser.add_argument("coly", nargs="+", type=str, help="The column(s) to plot on the y-axis.")
        parser.add_argument("--colx", type=str, default="Time",
                            help="The column to plot on the x-axis. Defaults to 'Time'.")
        parser.add_argument("-n","--name", type=str, help="The name of the graph.", required=True)
        parser.add_argument("--x-limit", nargs=2, type=float, default=[None, None],
                            help="The lower and upper limits of the x-axis.")
        parser.add_argument("--y-limit", nargs=2, type=float, default=[None, None],
                            help="The lower and upper limits of the y-axis.")
        parser.add_argument("--y-axis-label", type=str, default="Values",
                            help="The label for the y-axis. Defaults to 'Values'.")
        parser.add_argument("--save-plot", action="store_true", help="Whether to save the plot as an image.")
        parser.add_argument("-t","--timing", choices=["sec", "min", "hour", "date"], default="min",
                            help="The timing unit for the x-axis. Can be 'sec', 'min', 'hour', or 'date'. Defaults to 'min'.")
        parser.add_argument("--y-line", type=int, help="The y-coordinate of a horizontal line to add to the plot.")
        parser.add_argument("--y-line-label", type=str, help="The label for the y-line.")
        parser.add_argument("--start-date", type=str, default=None,
                            help="The start date \"YEAR.MONTH.DAY_HOUR:MIN:SEC\"for the x-axis.")
        parser.add_argument("--end-date", type=str, default=None,
                            help="The end date \"YEAR.MONTH.DAY_HOUR:MIN:SEC\"for the x-axis.")
        parser.add_argument("--other-coly", type=str, nargs="+", help="The column(s) to plot on the twin y-axis.")
        parser.add_argument("--other-coly-name", type=str, help="The label for the twin y-axis. Defaults to 'Values'.")

        # Parse the command-line arguments
        args = parser.parse_args()

        # Call your function with the parsed arguments
        get_graph_from_file(args.file, args.coly, colx=args.colx, name=args.name, x_limit=args.x_limit,
                            y_limit=args.y_limit, ax_y_name=args.y_axis_label,
                            is_saving=args.save_plot, timing=args.timing, put_y_line=args.y_line,
                            y_line_name=args.y_line_label, start_date=args.start_date, end_date=args.end_date,
                            other_coly=args.other_coly, other_coly_name=args.other_coly_name
                            )

        # To get graph of tensions and length from Linux File on the terminal
        # python -m src.get_graph "RecordMonitoring_2023.06.12_09-06-37.txt" "Tension2" "Tension4" --y-axis-label "Tension (N)" -n "Tension-2-4" --colx "LinuxTime" --start-date "2023.06.12_11:50:00" --other-coly "Length2" "Length4" "LengthTot" --other-coly-name "Rope Length (cm)"

        # To get graph of temperatures from Windows File on the terminal
        # python -m src.get_graph "copy_cern_data_run29.txt" "Ta" "Tb" "Tc" "Td" --y-axis-label "Temperature (°C)" --colx "Time" -t "hour" --name "graph_weekend" --start-date "2023.06.09_18:00:00" --y-limit -200 -90 --y-line -186

        # To get the graph of temperatures from the 32 data appended
        # python -m src.get_graph "final_data32.txt" "Ta" "Tb" "Tc" "Td" --y-axis-label "Temperature (°C)" --colx "Time" -t "hour" --name "temperature_since_friday_18:00" --start-date "2023.06.09_18:00:00" --y-limit -200 -90 --y-line -186

    else:
        print("use src.main --help")

else:

    print("----- Début programme depuis get_graph.py -----")

    get_graph_from_file("copy_cern_data_run29.txt", coly=["Ta", "Tb", "Tc", "Td"],
                        name="test1", timing="hour",
                        ax_y_name="Temperature (°C)"
                        )
    get_graph_from_file("RecordMonitoring_2023.06.10_14.28.48.txt", coly=["Tension2", "Tension4"], colx="LinuxTime",
                        name="motor_graph", timing="min", end_date= "2023.06.10_15:30:48",
                        ax_y_name="Tension (N)"
                        )
    print("----- Fin programme -----")
