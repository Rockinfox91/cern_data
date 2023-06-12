import numpy as np
import pandas as pd
from datetime import timedelta, datetime
from src.process.data_analyse import lire_data


def get_secondstep_from_time(timewanted: str, startdate: datetime):
    """
    Calculates the number of seconds between the specified time and the start date.

    Args:
        timewanted (str): The desired time in the format "YYYY-MM-DD HH:MM:SS".
        startdate (datetime): The start date.

    Returns:
        int: The number of seconds as an integer.
    """
    timewanted_datetime = datetime.strptime(timewanted, "%Y-%m-%d %H:%M:%S")
    difference = timewanted_datetime - startdate
    return int(difference.total_seconds())


def get_minutestep_from_time(timewanted: str, startdate: datetime):
    """
    Calculates the number of minutes between the specified time and the start date.

    Args:
        timewanted (str): The desired time in the format "YYYY-MM-DD HH:MM:SS".
        startdate (datetime): The start date.

    Returns:
        int: The number of minutes as an integer.
    """
    return get_secondstep_from_time(timewanted, startdate) // 60


def get_time_from_secondstep(secondstep: int, startdate: datetime):
    """
    Calculates the time from the specified number of seconds and the start date.

    Args:
        secondstep (int): The number of seconds.
        startdate (datetime): The start date.

    Returns:
        str: The calculated time in the format "YYYY-MM-DD HH:MM:SS".
    """
    wanted_date = startdate + timedelta(seconds=secondstep)
    return wanted_date.strftime("%Y-%m-%d %H:%M:%S")


def get_date_first_data(file: str) -> datetime:
    """
    Retrieves the datetime of the first data point in the specified file.

    Args:
        file (str): The name of the file.

    Returns:
        datetime: The datetime of the first data point.
    """
    filename = f"data/{file}"
    donnees = np.genfromtxt(filename, delimiter='\t', skip_header=1)
    date = donnees[0][0] - 263
    realdate = datetime.fromtimestamp(date)
    return realdate


def get_date_last_data(file: str) -> datetime:
    """
    Retrieves the datetime of the last data point in the specified file.

    Args:
        file (str): The name of the file.

    Returns:
        datetime: The datetime of the last data point.
    """
    filename = f"data/{file}"
    donnees = np.genfromtxt(filename, delimiter='\t', skip_header=1)
    date = donnees[-1][0] - 263
    realdate = datetime.fromtimestamp(date)
    return realdate


def get_unix_time_from_date(date: str) -> float:
    """
    Converts the specified date string to a Unix timestamp.

    Args:
        date (str): The date in the format "YYYY.MM.DD_HH:MM:SS".

    Returns:
        float: The Unix timestamp.
    """
    date_format = "%Y.%m.%d_%H:%M:%S"
    datetime_obj = datetime.strptime(date, date_format)
    unix_timestamp = datetime_obj.timestamp()
    return int(unix_timestamp)


def merge_dataframes_by_unix(df1: pd.DataFrame, df2: pd.DataFrame):
    """
    Merges two DataFrames based on the UnixTimestamp column.

    Args:
        df1 (pd.DataFrame): The first DataFrame.
        df2 (pd.DataFrame): The second DataFrame.

    Returns:
        pd.DataFrame: The merged DataFrame.
    """
    df1.rename(columns={"Time": "UnixTimestamp"}, inplace=True)
    df2.rename(columns={"LinuxTime": "UnixTimestamp"}, inplace=True)
    df1["UnixTimestamp"] = df1["UnixTimestamp"].astype(int)
    df2["UnixTimestamp"] = df2["UnixTimestamp"].astype(int)
    merged_df = pd.merge(df1, df2, on="UnixTimestamp", how="inner")
    return merged_df