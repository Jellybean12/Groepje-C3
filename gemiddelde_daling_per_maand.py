import pandas as pd
from sqlalchemy import create_engine
import datetime
import numpy as np

def create_dataframe_from_query(url, query) :
    """Maakt een connectie met een database met de meegegeven url. Met de query wordt een dataframe gemaakt."""
    engine = create_engine(url)
    df = pd.read_sql(query, engine)
    return df

# De query gebruikt test_data
url = 'postgresql://postgres:Welkom01!@10.30.1.10:5432/POC'
query = """SELECT * 
FROM meting 
WHERE pnt_id = 'L450745P202580' OR pnt_id = 'L450805P203520' OR pnt_id = 'L450815P203485' OR pnt_id = 'L450825P203555' OR pnt_id = 'L450870P203080' 
ORDER BY datum"""
df = create_dataframe_from_query(url, query)


def average(df):
    """Returnt het gemiddelde van alle metingen in de meegegeven dataframe."""
    count = len(df['meting'])
    measurement = df['meting']
    total_sum = measurement.sum()
    average = (total_sum / count)

    return average


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


def average_measurement_per_month(df):
    """Functie die een dataframe returnt met per maand in een jaar de gemiddelde meting."""
    dataframe = df[:]

    # De waardes in de datum kolom worden omgezet naar datetime, zodat er daaronder op basis van deze kolom
    # berekend kan worden wat het eerste jaar en wat het laatste jaar is waarbinnen de metingen plaatsvinden
    dataframe['datum'] = pd.to_datetime(dataframe['datum'])
    minyear = dataframe['datum'].min().year
    maxyear = dataframe['datum'].max().year

    dataframe = remove_first_measurement(dataframe)

    result = pd.DataFrame(columns=['jaar_maand', 'gemiddelde'])

    # Door de jaren heen loopen
    for x in range(minyear, maxyear + 1):
        # Door de maanden in het betreffende jaar loopen
        for y in range(1, 13):
            # Per maand worden begin- en einddatum verzameld en worden de datums
            # berekend die binnen dat begin en einde vallen
            start_month = pd.Timestamp(year=x, month=y, day=1)
            end_month = start_month.to_period('M').to_timestamp('M')
            this_month = (dataframe['datum'] > start_month) & (dataframe['datum'] <= end_month)

            # Er wordt een dataframe voor de betreffende maand gemaakt
            this_month = dataframe.loc[this_month]
            # Wanneer er metingen zijn in de maand, wordt het gemiddelde berekend
            # Wanneer er geen metingen zijn, gebeurt er niks
            if not this_month.empty:
                year_month = str(x) + str(y)
                avg = average(this_month)
                # Aan de result dataframe wordt een nieuwe regel toegevoegd met het jaar, de maand en het gemiddelde
                result = result.append({'jaar_maand': year_month, 'gemiddelde': avg}, ignore_index=True)

    return result

resultdf = average_measurement_per_month(df)