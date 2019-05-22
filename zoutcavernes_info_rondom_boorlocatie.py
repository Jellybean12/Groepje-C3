# Dit is er nodig
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import geopy.distance

# Onderstaand is om pandas de dataframes goed te laten weergeven (zodat er niet maar de helft van een dataframe wordt geprint).
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 10)

# De connectie met de database wordt gemaakt.
engine = create_engine('postgresql://postgres:Welkom01!@10.30.1.10:5432/POC')


def get_dest_from_point(latitude, longitude, meters, richting):
    """Berekent de minimale en maximale latitudes en longitudes van een punt."""
    kilometer = meters / 1000

    # Maak het startpunt, door middel van de meegegeven latitude en longitude
    start = geopy.Point(latitude, longitude)

    # Maak een distance object met de aangegeven meters
    d = geopy.distance.distance(kilometers=kilometer)

    # Gebruik de destination methode steeds met een andere degree voor bearing, dat verschilt namelijk voor
    # noord, oost, zuid en west
    dest = d.destination(point=start, bearing=richting)
    return dest


def radiusbepaler(boorpunt, meters):
    """Returnt een dataframe gevuld met de boorlocaties en de desbetreffende radius in meters.
    Er kan een dataset in gestopt worden met boor locaties. Per locatie wordt dan de minimale en de maximale
    lon en lat gereturnd."""

    endlist = pd.DataFrame(columns=['BoorID', 'Locatie', 'MaxLat', 'MinLat', 'MaxLon', 'MinLon'])

    boorid = boorpunt['boor_id'][0]
    locatie = boorpunt['locatie'][0]
    maxlat = get_dest_from_point(boorpunt['boor_lat'][0], boorpunt['boor_lon'][0], meters, 0).latitude
    minlat = get_dest_from_point(boorpunt['boor_lat'][0], boorpunt['boor_lon'][0], meters, 180).latitude
    maxlon = get_dest_from_point(boorpunt['boor_lat'][0], boorpunt['boor_lon'][0], meters, 90).longitude
    minlon = get_dest_from_point(boorpunt['boor_lat'][0], boorpunt['boor_lon'][0], meters, 270).longitude

    endlist = endlist.append(
        {'BoorID': boorid, 'Locatie': locatie, 'MaxLat': maxlat, 'MinLat': minlat, 'MaxLon': maxlon, 'MinLon': minlon},
        ignore_index=True)
    return endlist


def koppel_meetpunten(datasetboorlocatie, radius):
    """Koppelt de meetpunten aan een boorlocatie zodra die binnen de opgegeven radius zitten."""
    returndata = pd.DataFrame()
    boor_locaties_met_radius = radiusbepaler(datasetboorlocatie, radius)

    for boor_index, boor_row in boor_locaties_met_radius.iterrows():
        max_lat = boor_row['MaxLat']
        min_lat = boor_row['MinLat']
        max_lon = boor_row['MaxLon']
        min_lon = boor_row['MinLon']

        query_lat_lon = """SELECT *
        FROM pnt_locatie
        WHERE pnt_lat <= '""" + str(max_lat) + """'
        AND pnt_lat >= '""" + str(min_lat) + """'
        AND pnt_lon <= '""" + str(max_lon) + """'
        AND pnt_lon >= '""" + str(min_lon) + """'"""

        row = pd.read_sql_query(query_lat_lon, engine)
        returndata = returndata.append(row, ignore_index=True)

    return returndata


def get_metingen(df):
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


def min_measurement(df):
    return df['meting'].min()


def max_measurement(df):
    return df['meting'].max()


def avg_measurement(df):
    return df['meting'].mean()


def info_punten_rondom_boorlocatie(boorid, radius_dichtbij, radius_ver_weg):
    """Print van het nabije gebied en het gebied verder weg van een boorlocatie de maximale stijging, de maximale daling en de gemiddelde daling.
    Er wordt een boorid meegegeven. Er wordt twee keer een radius meegegeven. De eerste radius
    is de radius voor dichtbij. De tweede is die voor verder weg."""

    # De gegevens van het meegegeven boorid worden opgehaald uit de database
    q = "SELECT * FROM boor_locatie WHERE boor_id = "
    booridaddon = "'" + str(boorid) + "'"
    boor_query = q + booridaddon
    boorpunt = pd.read_sql_query(boor_query, engine)

    # Er worden nu twee dataframes gemaakt. Namelijk de gekoppelde punten binnen de kleine radius
    # en de gekoppelde punten binnen de grote radius.
    inner_radius_points = koppel_meetpunten(boorpunt, radius_dichtbij)
    whole_radius_points = koppel_meetpunten(boorpunt, radius_ver_weg)

    # De dataframes woreden bij elkaar gevoegd en vervolgens worden de duplicates eruit verwijderd
    # Zo ontstaat er een dataframe die punten heeft in de buitenste radius, die niet in de binnenste radius zitten
    merge_radius_points = inner_radius_points.append(whole_radius_points, ignore_index=True)
    outer_radius_points = merge_radius_points.drop_duplicates(subset='pnt_id', keep=False)

    # De bijbehorende metingen worden opgehaald en in dataframes gezet
    measurements_inner_radius = get_metingen(inner_radius_points)
    measurements_outer_radius = get_metingen(outer_radius_points)

    print("Max daling: " , min_measurement(
        measurements_inner_radius) , " meter\nMax stijging: " , max_measurement(
        measurements_inner_radius) , " meter\nGem daling/stijging: " , avg_measurement(
        measurements_inner_radius) , " meter.\nMax daling van het omliggende gebied: " , min_measurement(
        measurements_outer_radius) , " meter\nMax stijging van het omliggende gebied: " , max_measurement(
        measurements_outer_radius) , " meter\nGem daling/stijging van het omliggende gebied: " , avg_measurement(
        measurements_outer_radius) , " meter.")


info_punten_rondom_boorlocatie(477, 100, 400)
