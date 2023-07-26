# Cern data programs

To see this file from a linux prompt, copy/paste in the console :


````sh
pandoc README.md | lynx -stdin
````

# Installation
(only if you want to copy this on another computer, pass this if you're on lxplus.)

## Clone the repository
````shell
git clone https://github.com/Rockinfox91/cern_data.git
cd cern_data
python3 -m venv .venv
. ./.venv/bin/activate
pip install -r requirements.txt
````

# General information :

This module analyse data from the LN2 cold test experiment on DarkSide-20k.

This module is located in a virtual environment on the lxplus, to access it, do :

````shell
. ./.venv/bin/activate
````

You're now on the python VirtualENVironment. You can now use the module.

# How to use module :

This module is composed of several executable .py files located in /src, to access a certain file,
(let's say /src/get_graph.py) do python3 -m src.[name_of_the_file] (here python3 -m src.get_graph) without
the .py extension !!

To have help on how to use options for a file, do
````shell
python3 -m src.[file] -h
````

## get_graph
Generate a graph from data in a file.
````shell
python3 -m src.get_graph file [columns] [options]
````
### Examples
To get graph of tension on all data : 
````shell
python3 -m src.get_graph "linux_final_data" "Tension2" "Tension4" --y-axis-label "Tension (N)" -n "Tension-2-4" --colx "LinuxTime" --timing "day" --y-limit 0 60
````
To get the graph of temperatures from all data
````shell
python3 -m src.get_graph "windows_final_data" "Ta" "Tb" "Tc" "Td" --y-axis-label "Temperature (°C)" --colx "Time" -t "day" --name "temperature_since_friday_18:00" --start-date "2023.06.09_18:00:00" --y-limit -200 -90 --y-line -186
````
To get graph of length from linux file for stress test
````shell
python3 -m src.get_graph "RecordMonitoring_2023.06.14_09-25-42" "Tension2" "Tension4" --y-axis-label "Tension (N)" -n "Tension-2-4" --colx "LinuxTime" --start-date "2023.06.14_10:15:00" --timing "min" --y-limit 0 35
````
To get graph of length from linux file for calibration test
````shell
python3 -m src.get_graph "RecordMonitoring_2023.06.15_09-03-15" "Tension2" "Tension4" --y-axis-label "Tension (N)" -n "Tension-2-4" --colx "LinuxTime" --start-date "2023.06.15_13:35:00" --end-date "2023.06.15_17:32:00" --timing "hour" --y-limit 0 35
````

## calib_graph
To get the calibration test scatter plot.
````shell
python3 -m src.calib_graph
````

## append_data
Generate a file from all file data given. Not needed if there is no new data.
````shell
python3 -m src.append_data file1 sorting_column finalname [options]
````

### Examples
To get all linux files appended:
````shell
python3 -m src.append_data "RecordMonitoring" "LinuxTime" "linux_final_data" -a
````
To get all windows files appended:
````shell
python3 -m src.append_data "copy_cern" "Time" "windows_final_data" -a
````

## correlation
Plot correlation matrix for data files.
````shell
python3 -m src.correlation files [options]
````

### Examples
To get a correlation graph of both Windows and Linux datas :
````shell
python3 -m src.correlation "linux_final_data" "windows_final_data" -m -ec "CryoL" "FlowIn" "Hin" -t "Linear Correlation between LinuxData and WindowsData"
````