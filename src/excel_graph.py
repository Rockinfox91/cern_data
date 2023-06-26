import pandas as pd
import matplotlib.pyplot as plt

from src.process.data_analyse import lire_exel_data
from src.process.time_thing import get_unix_time_from_date
from src.process.graph import get_graph_from_file

if __name__ == "__main__":

    df = lire_exel_data("DSlevelfrom9t26june")

    # Convert "Timestamp (UTC_TIME)" column to datetime objects
    df['Timestamp (UTC_TIME)'] = pd.to_datetime(df['Timestamp (UTC_TIME)'])

    # Convert datetime objects to Unix timestamps
    df['UnixTimestamp'] = df['Timestamp (UTC_TIME)'].apply(lambda x: x.timestamp())

    date = {
        "2023.06.09_08:00:00" : 270,
        "2023.06.10_08:00:00": 250,
        "2023.06.11_08:00:00": 120,
        "2023.06.13_08:00:00": 250,
    }

    for date,value in date.items():
        df.loc[df["UnixTimestamp"] > get_unix_time_from_date(date), "value"] = value

    # Print the updated DataFrame
    print(df)

    get_graph_from_file(df, coly="Value %", colx="UnixTimestamp"
                        , name = "flux_tank", y_limit=[30,100], ax_y_name="% LN2 in tank",
                        timing="day",

                        )
