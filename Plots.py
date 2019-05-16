#modules importeren
import re
import math
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm
import sqlite3
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import datetime

#functies van Ralphine voor average dingen
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
                    half_year = str(x) + '-1'
                else:
                    half_year = str(x) + '-2'

                avg = average(this_half)
                result = result.append({'pnt_id': pnt_id, 'halfjaar': half_year, 'gemiddelde': avg}, ignore_index=True)

    return result


def remove_first_measurement(df):
    """Deze functie verwijderd per uniek punt in het meegegeven dataframe de eerste (0-)meting."""
    result = df[:]

    # Per uniek pnt_id wordt de eerste meting verwijderd uit het dataframe.
    # Dit omdat de eerste meting altijd 0 is en die ervoor zou zorgen dat het gemiddelde niet zou kloppen
    for i in result.pnt_id.unique():
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

def reg_plot_all_pnt_meting(df,w,h):
    """Deze functie maakt een regressie plot van een DataFrame. Gebruikende datum_ordinal als x en meting als y"""
    df['date_ordinal'] = pd.to_datetime(df['datum']).apply(lambda date: date.toordinal())
    plt.figure(figsize=(w,h))
    ax = sns.regplot(
        data=df,
        x='date_ordinal',
        y='meting')
    ax.set_title(title)
    ax.set_xlabel('Datum')
    ax.set_ylabel('Gemiddelde daling in meters')
    ax.set_xticklabels(df['datum'].astype(str))

#functies om plot te maken
def line_plot_average_half_year(df,w,h):
    """Deze functie maakt een lijn plot van een DataFrame.
    Gebruikt een df die aangemaakt is door de functie per_unique_point_average_half_year.
    Gebruikende halfjaar als x en gemiddelde als y"""
    data = per_unique_point_average_half_year(df)
    plt.figure(figsize=(w,h))
    ax = sns.lineplot(
        data=data,
        x='halfjaar',
        y='gemiddelde',
        legend = False)
    ax.set_xlabel('Datum per halfjaar')
    ax.set_ylabel('Gemiddelde daling in meters')
    ax.set_title(title)
    plt.savefig('C:\\TEMP\\'+loc+'.png')
    #fig = ax.get_figure()
    #fig.savefig('C:\\TEMP\\test.png')

engine = create_engine('postgresql://postgres:Welkom01!@10.30.1.10:5432/POC')
loc = 'SintJansKlooster'
query = """SELECT * FROM meting WHERE pnt_id IN (SELECT pnt_id FROM pnt_locatie WHERE locatie = '""" + loc + """') and sat_id = '10'"""
df = pd.read_sql(query, con=engine)

#df = pd.DataFrame()
#for chunk in tqdm(result):
#    df = pd.concat(([df,chunk]))

title = 'Bodemdaling ' + loc

#data = per_unique_point_average_half_year(df)
line_plot_average_half_year(df,20,8)
