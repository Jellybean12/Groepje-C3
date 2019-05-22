# modules importeren
import pandas as pd
from sqlalchemy import create_engine
import datetime
import numpy as np
import re
import math
import matplotlib.pyplot as plt


def create_dataframe_from_query(url, query):
    """Maakt een connectie met een database met de meegegeven url. Met de query wordt een dataframe gemaakt."""
    engine = create_engine(url)
    df = pd.read_sql(query, engine)
    return df


# Engine connectie opzetten en een dataframe maken
url = 'postgresql://postgres:Welkom01!@10.30.1.10:5432/POC'
query = """SELECT * FROM meting WHERE pnt_id IN (SELECT pnt_id FROM pnt_locatie WHERE locatie = 'Hammerflier' LIMIT 1000)"""
df = create_dataframe_from_query(url, query)


def per_unique_point_average_half_year(bigdataframe):
    """Returnt een dataframe met per uniek pnt_id van de meegegeven dataframe per halfjaar het
    gemiddelde van de metingen van dat punt."""
    dataframe = bigdataframe[:]

    # De waardes in de datum kolom worden omgezet naar datetime
    dataframe['datum'] = pd.to_datetime(dataframe['datum'])
    # De eerste (0-)meting van elk uniek pnt_id wordt uit de dataframe gehaald
    dataframe = remove_first_measurement(dataframe)

    result = pd.DataFrame(columns=['pnt_id', 'halfjaar', 'gemiddelde'])

    # Voor elk uniek punt dat voorkomt in de meegegeven dataframe, wordt een dataframe gemaakt met per halfjaar het
    # gemiddelde van alle metingen van dat punt in dat halfjaar. Telkens wordt deze 'kleine' dataframe aan de grote,
    # resulterende dataframe toegevoegd.
    for pnt_id in dataframe.pnt_id.unique():
        mini = average_measurement_per_half_year(dataframe.loc[dataframe['pnt_id'] == pnt_id], pnt_id)
        result = result.append(mini, ignore_index=True)
    return result


def average_measurement_per_half_year(df, id):
    """Functie die een dataframe returnt met per halfjaar de gemiddelde meting van een punt. Er wordt een
    dataframe meegegeven met daarin het id, pnt_id, datum, meting en sat_id van een meting.
    Ook wordt er een pnt_id mee gegeven, zodat deze gebruikt kan worden in het maken van de resulterende dataframe."""
    dataframe = df[:]

    # Op basis van de data kolom wordt berekend wat het eerste en laatste jaar is waarbinnen de metingen plaatsvinden
    minyear = dataframe['datum'].min().year
    maxyear = dataframe['datum'].max().year

    result = pd.DataFrame(columns=['pnt_id', 'halfjaar', 'gemiddelde'])
    pnt_id = id

    # Door de jaren heen loopen
    for x in range(minyear, maxyear + 1):
        # Door de twee halve jaren van het betreffende jaar heen loopen
        for y in range(1, 8, 6):
            # De start en het einde van het halfjaar  berekenen
            start_half = pd.Timestamp(year=x, month=y, day=1)
            end_month = pd.Timestamp(year=x, month=y + 5, day=1)
            end_half = end_month.to_period('M').to_timestamp('M')
            # De metingen selecteren die binnen het halfjaar liggen
            this_half = (dataframe['datum'] > start_half) & (dataframe['datum'] <= end_half)
            this_half = dataframe.loc[this_half]

            # Wanneer er metingen zijn binnen het halfjaar, hiervan het gemiddelde berekenen en toevoegen aan de resulterende dataframe
            if not this_half.empty:
                if y == 1:
                    half_year = str(x) + '1'
                else:
                    half_year = str(x) + '2'

                avg = average(this_half)
                result = result.append({'pnt_id': pnt_id, 'halfjaar': half_year, 'gemiddelde': avg}, ignore_index=True)

    return result


def remove_first_measurement(df):
    """Deze functie verwijderd per uniek punt in het meegegeven dataframe de eerste (0-)meting."""
    result = df[:]

    # Per uniek pnt_id wordt de eerste meting verwijderd uit het dataframe.
    # Dit omdat de eerste meting altijd 0 is en die ervoor zou zorgen dat het gemiddelde niet zou kloppen
    for i in result.pnt_id.unique():
        # Maak per uniek punt een dataframe met zijn metingen
        df_per_pnt = result.loc[result['pnt_id'] == i]
        # Check hoeveel sat_id's die metingen hebben gedaan
        aantal_sat_ids = df_per_pnt.sat_id.unique()

        # Als er meerdere satellieten de metingen hebben gedaan, loop dan door de satellieten heen
        if len(aantal_sat_ids) != 1:
            for j in aantal_sat_ids:
                df_per_sat = df_per_pnt.loc[df_per_pnt['sat_id'] == j]
                ind = df_per_sat.index.values[0]
                result = result.drop(index=ind)
        else:
            df_per_pnt = result.loc[result['pnt_id'] == i]
            ind = df_per_pnt.index.values[0]
            result = result.drop(index=ind)

    return result


def average(df):
    """Returnt het gemiddelde van alle metingen in de meegegeven dataframe."""
    count = len(df['meting'])
    measurement = df['meting']
    total_sum = measurement.sum()
    average = (total_sum / count)

    return average


data = per_unique_point_average_half_year(df)
