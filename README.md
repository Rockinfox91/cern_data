# Cern data programs

To see this file from a linux prompt, copy/paste in the console :


````sh
pandoc README.md | lynx -stdin
````

# General information :

blabla

To have help on how to use options for a file, do
````shell
python3 -m src.[file] -h
````

# How to use module :

## get_graph
Generate a graph from data in a file.
````shell
python3 -m src.get_graph file [columns] [options]
````
### Examples
To get graph of tension on all data : 
````shell
python -m src.get_graph "linux_final_data" "Tension2" "Tension4" --y-axis-label "Tension (N)" -n "Tension-2-4" --colx "LinuxTime" --timing "day" --y-limit 0 60
````
To get the graph of temperatures from all data
````shell
python -m src.get_graph "windows_final_data" "Ta" "Tb" "Tc" "Td" --y-axis-label "Temperature (°C)" --colx "Time" -t "day" --name "temperature_since_friday_18:00" --start-date "2023.06.09_18:00:00" --y-limit -200 -90 --y-line -186
````
To get graph of length from linux file for afternoon program
````shell
python -m src.get_graph "RecordMonitoring_2023.06.14_09-25-42" "Tension2" "Tension4" --y-axis-label "Tension (N)" -n "Tension-2-4" --colx "LinuxTime" --start-date "2023.06.16_13:35:00" --end-date "2023.06.16_17:40:00" --timing "hour" --y-limit 0 35
````

## append_data
Generate a file from all file data given.
````shell
python3 -m src.append_data file1 sorting_column finalname [options]
````

### Examples
To get all linux files appended:
````shell
python -m src.append_data "RecordMonitoring" "LinuxTime" "linux_final_data" -a
````
To get all windows files appended:
````shell
python -m src.append_data "copy_cern" "Time" "windows_final_data" -a
````

## calib_graph
To get the calibration test scatter plot.
````shell
python3 -m src.calib_graph
````

## correlation
Plot correlation matrix for data files.
````shell
python3 -m src.correlation files [options]
````

### Examples
To get a correlation graph of both Windows and Linux datas :
````shell
python -m src.correlation "linux_final_data" "windows_final_data" -m -ec "CryoL" "FlowIn" "Hin" -t "Linear Correlation between LinuxData and WindowsData"
````