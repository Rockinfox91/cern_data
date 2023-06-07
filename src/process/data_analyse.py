import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import timedelta,datetime
import os


def get_secondstep_from_time(timewanted: str,startdate: datetime):
    timewanted_datetime = datetime.strptime(timewanted, "%Y-%m-%d %H:%M:%S")

    difference = timewanted_datetime - startdate  # Calcule la différence de temps entre la date voulue et le temps de début d'acquisition

    return int(difference.total_seconds())  # Renvoyer le nombre de secondes sous forme d'entier


def get_minutestep_from_time(timewanted: str, startdate: datetime):
    return get_secondstep_from_time(timewanted,startdate)//60


def get_time_from_secondstep(secondstep: int, startdate: datetime):
    wanted_date = startdate + timedelta(seconds=secondstep)
    return wanted_date.strftime("%Y-%m-%d %H:%M:%S")


def get_creation_date_of_file(file: str) -> datetime:
    filename = f"data/{file}.txt"
    file_creation_time = os.path.getctime(filename)
    file_creation_datetime = pd.to_datetime(file_creation_time, unit='s')
    file_creation_datetime += timedelta(hours=2)
    return file_creation_datetime
