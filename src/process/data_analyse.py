import numpy as np
import pandas as pd
from datetime import timedelta,datetime


def get_secondstep_from_time(timewanted: str,startdate: datetime):
    timewanted_datetime = datetime.strptime(timewanted, "%Y-%m-%d %H:%M:%S")

    difference = timewanted_datetime - startdate  # Calcule la différence de temps entre la date voulue et le temps de début d'acquisition

    return int(difference.total_seconds())  # Renvoyer le nombre de secondes sous forme d'entier


def get_minutestep_from_time(timewanted: str, startdate: datetime):
    return get_secondstep_from_time(timewanted,startdate)//60


def get_time_from_secondstep(secondstep: int, startdate: datetime):
    wanted_date = startdate + timedelta(seconds=secondstep)
    return wanted_date.strftime("%Y-%m-%d %H:%M:%S")


def get_date_first_data(file: str) -> datetime:
    filename = f"data/{file}.txt"
    donnees = np.genfromtxt(filename,
                            delimiter='\t', skip_header=1)
    # Étiquettes des colonnes
    date = donnees[0][0] - 263
    realdate = datetime.fromtimestamp(date)
    return realdate
def get_date_last_data(file: str) -> datetime:
    filename = f"data/{file}.txt"
    donnees = np.genfromtxt(filename,
                            delimiter='\t', skip_header=1)
    # Étiquettes des colonnes
    date = donnees[-1][0] - 263
    realdate = datetime.fromtimestamp(date)
    return realdate


