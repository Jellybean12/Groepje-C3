# Dit is er nodig
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# Onderstaand is om pandas de dataframes goed te laten weergeven (zodat er niet maar de helft van een dataframe wordt geprint).
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 10)

# De connectie met de database wordt gemaakt.
engine = create_engine('postgresql://postgres:Welkom01!@10.30.1.10:5432/POC')

def meters_naar_graden(meters) :
    """Rekent meters om naar graden"""
    graden = (meters / 30.92) / 3600
    return graden

def radiusbepaler(dataset, meters) :
    """Returnt een dataframe gevuld met de boorlocaties en de desbetreffende radius in meters.
    Er kan een dataset in gestopt worden met boor locaties. Per locatie wordt dan de minimale en de maximale
    lon en lat gereturnd."""

    endlist = pd.DataFrame()

    graden = meters_naar_graden(meters)

    for row in dataset:
        boorid = endlist["BoorID"] = dataset.loc[:, 'boor_id']
        locatie = endlist["Locatie"] = dataset.loc[:, 'locatie']
        maxlon = endlist["MaxLon"] = dataset.loc[:, 'boor_lon'] + graden
        minlon = endlist["MinLon"] = dataset.loc[:, 'boor_lon'] - graden
        maxlat = endlist["MaxLat"] = dataset.loc[:, 'boor_lat'] + graden
        minlat = endlist["MinLat"] = dataset.loc[:, 'boor_lat'] - graden

    return endlist

def koppel_meetpunten(datasetmeetpunten, datasetboorlocatie, radius) :
    """Koppelt de meetpunten aan een boorlocatie zodra die binnen de opgegeven radius zitten."""
    punten = []
    boor_locaties_met_radius = radiusbepaler(datasetboorlocatie, radius)

    # Door alle punten heen loopen die zijn meegegeven
    for index, row in datasetmeetpunten.iterrows():
        # Door boor_locaties heen loopen
        for boor_index, boor_row in boor_locaties_met_radius.iterrows():
            # Check of de lon en lat van een betreffend meetpunt binnen de betreffende radius valt
            if row['pnt_lon'] <= boor_row['MaxLon'] and row['pnt_lon'] >= boor_row['MinLon'] and row[
                'pnt_lat'] <= boor_row['MaxLat'] and row['pnt_lat'] >= boor_row['MinLat'] :
                boorid = boor_row['BoorID']
                locatie = boor_row['Locatie']
                minlon = boor_row['MinLon']
                maxlon = boor_row['MaxLon']
                minlat = boor_row['MinLat']
                maxlat = boor_row['MaxLat']
                pnt_id = row['pnt_id']
                pnt_lon = row['pnt_lon']
                pnt_lat = row['pnt_lat']
                punten.append([boorid, locatie, minlon, maxlon, minlat, maxlat, pnt_id, pnt_lon, pnt_lat])
    returndata = pd.DataFrame(punten,
                              columns=['boorid', 'locatie', 'minlon', 'maxlon', 'minlat', 'maxlat', 'pnt_id',
                                       'pnt_lon', 'pnt_lat'])

    return returndata

def get_metingen(df) :
    """Returnt een dataframe met alle metingen van de punten uit de meegegeven dataframe.
    Gebruikt het dataframe die aangemaakt is door de functie meetpuntenkoppelen."""
    templist = []
    # Alle pnt_id's uit het meegegeven dataframe worden aan elkaar gekoppeld in één string, en worden gescheiden door een komma
    ids = "', '".join(df['pnt_id'])
    # Alle pnt_id's uit de meegegeven dataframe worden opgehaald uit de tabel meting
    select_query = """SELECT * FROM meting WHERE pnt_id IN ('""" + ids + """')"""
    result = pd.read_sql_query(select_query, engine)
    for index, row in result.iterrows():
        id = row['id']
        pnt_id = row['pnt_id']
        datum = row['datum']
        meting = row['meting']
        sat_id = row['sat_id']
        templist.append([id, pnt_id, datum, meting, sat_id])
    return pd.DataFrame(templist, columns=['id', 'pnt_id', 'datum', 'meting', 'sat_id'])

def min_measurement(df) :
    return df['meting'].min()

def max_measurement(df) :
    return df['meting'].max()

def avg_measurement(df) :
    return df['meting'].mean()

def punten_rondom_boorlocatie(boorid, radius_dichtbij, radius_ver_weg) :
    """Print van het nabije gebied en het gebied verder weg van een boorlocatie de maximale stijging, de maximale daling en de gemiddelde daling.
    Er wordt een boorid meegegeven. Er wordt twee keer een radius meegegeven. De eerste radius
    is de radius voor dichtbij. De tweede is die voor verder weg."""

    # Alle punten worden opgehaald
    alle_punten = pd.read_sql_query('SELECT * FROM pnt_locatie', engine)

    # De gegevens van het meegegeven boorid worden opgehaald uit de database
    q = "SELECT * FROM boor_locatie WHERE boor_id = "
    booridaddon = "'" + str(boorid) + "'"
    boor_query = q + booridaddon
    boor_dataset = pd.read_sql_query(boor_query, engine)

    # Er worden nu twee dataframes gemaakt. Namelijk de gekoppelde punten binnen de kleine radius
    # en de gekoppelde punten binnen de grote radius.
    inner_radius_points = koppel_meetpunten(alle_punten, boor_dataset, radius_dichtbij)
    whole_radius_points = koppel_meetpunten(alle_punten, boor_dataset, radius_ver_weg)
    # De dataframes woreden bij elkaar gevoegd en vervolgens worden de duplicates eruit verwijderd
    # Zo ontstaat er een dataframe die punten heeft in de buitenste radius, die niet in de binnenste radius zitten
    merge_radius_points = inner_radius_points.append(whole_radius_points, ignore_index=True)
    outer_radius_points = merge_radius_points.drop_duplicates(subset='pnt_id', keep=False)

    # De bijbehorende metingen worden opgehaald en in dataframes gezet
    measurements_inner_radius = get_metingen(inner_radius_points)
    measurements_outer_radius = get_metingen(outer_radius_points)

    return print('maxdaling: ', min_measurement(measurements_inner_radius), 'Meter ', 'maxstijging: ', max_measurement(measurements_inner_radius), 'Meter ', 'gemdaling: ',
                 avg_measurement(measurements_inner_radius),
                 'Meter', ' maxdaling van het omliggende gebied: ', min_measurement(measurements_outer_radius), 'Meter ',
                 'maxstijging van het omliggende gebied: ', max_measurement(measurements_outer_radius), 'Meter ',
                 'gemdaling van het omliggende gebied: ', avg_measurement(measurements_outer_radius),
                 'Meter')


punten_rondom_boorlocatie(358, 10, 50)
