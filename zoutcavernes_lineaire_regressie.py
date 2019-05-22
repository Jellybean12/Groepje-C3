############# Deze file is aan gewerkt, maar is nooit afgekomen. De file werkt dus niet naar behoren, maar biedt wel mogelijk oplossingen voor de toekomst. #############

# De benodigde imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from sklearn import *

# Onderstaand is om pandas de dataframes goed te laten weergeven (zodat er niet maar de helft van een dataframe wordt geprint).
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 10)


def allesineen(boorid, radiusinmeter):
    ###########SQL stukje###########
    engine = create_engine('postgresql://postgres:Welkom01!@10.30.1.10:5432/POC')
    sqldataset = pd.read_sql_query('Select * From pnt_locatie', engine)
    sqldatasetboorquery = "Select * From boor_locatie where boor_id = "
    booridtostr = str(boorid)
    booridaddon = "'" + booridtostr + "'"
    booridcompletequery = sqldatasetboorquery + booridaddon
    sqldatasetboor = pd.read_sql_query(booridcompletequery, engine)

    def radiusbepaler(dataset, meters):
        # radiusbepaler zorgt ervoor dat er een dataframe gevult met de boorlocaties en de desbetreffende radius in meters wordt gereturned
        endlist = pd.DataFrame()

        def GradenNaarMeters(meters):
            graden = (meters / 30.92) / 3600
            return graden

        for row in dataset:
            boorid = endlist["BoorID"] = dataset.loc[:, 'boor_id']
            locatie = endlist["Locatie"] = dataset.loc[:, 'locatie']
            maxlon = endlist["MaxLon"] = dataset.loc[:, 'boor_lon'] + GradenNaarMeters(meters)
            minlon = endlist["MinLon"] = dataset.loc[:, 'boor_lon'] - GradenNaarMeters(meters)
            maxlat = endlist["MaxLat"] = dataset.loc[:, 'boor_lat'] + GradenNaarMeters(meters)
            minlat = endlist["MinLat"] = dataset.loc[:, 'boor_lat'] - GradenNaarMeters(meters)
        return endlist

    def meetpuntenkoppelen(datasetmeetpunten, datasetboorlocatie, radius):
        # deze functie zorgt ervoor dat de meetpunten gekoppeld worden aan een boorlocatie zodra die binnen de opgegeven radius zit
        punten = []
        meting = radiusbepaler(datasetboorlocatie, radius)
        for index, row in datasetmeetpunten.iterrows():
            for lijstje_index, lijstje_row in meting.iterrows():
                if row['pnt_lon'] <= lijstje_row['MaxLon'] and row['pnt_lon'] >= lijstje_row['MinLon'] and row[
                    'pnt_lat'] <= lijstje_row['MaxLat'] and row['pnt_lat'] >= lijstje_row['MinLat']:
                    boorid = lijstje_row['BoorID']
                    locatie = lijstje_row['Locatie']
                    minlon = lijstje_row['MinLon']
                    maxlon = lijstje_row['MaxLon']
                    minlat = lijstje_row['MinLat']
                    maxlat = lijstje_row['MaxLat']
                    pnt_id = row['pnt_id']
                    pnt_lon = row['pnt_lon']
                    pnt_lat = row['pnt_lat']
                    punten.append([boorid, locatie, minlon, maxlon, minlat, maxlat, pnt_id, pnt_lon, pnt_lat])
        returndata = pd.DataFrame(punten,
                                  columns=['boorid', 'locatie', 'minlon', 'maxlon', 'minlat', 'maxlat', 'pnt_id',
                                           'pnt_lon', 'pnt_lat'])
        return returndata

    # Dit is een tijdelijke work around voor niet schone data, dus punten waar je alleen de coordinaten hebt maar bijvoorbeeld niet de locatie en boornummer
    grondwaterontrekkinggebied = pd.DataFrame(
        {"boor_lon": [6.85581], "boor_lat": [52.35096], "Locatie": ['N/A'], "boor_id": ["N/A"]})
    # dit zijn de instellingen
    datameetpunten = meetpuntenkoppelen(sqldataset, sqldatasetboor, radiusinmeter)

    # dit is de select query die alle meetpunten sorteerd op punt id
    select_query = "select * from meting where pnt_id = "
    # tijdelijk lijstje
    metingentijdelijklijstje = []
    # eerste for loop zorgt voor de raw data die daarna nog per row uitgezocht moet worden zodra de tweede for loop klaar is -
    # dus per row gaat hij naar de volgende punt id en daar alle raw data van pakken

    for id in datameetpunten['pnt_id']:
        id2 = "'" + id + "'"
        var = select_query + id2
        result = pd.read_sql_query(var, engine)
        for index, row in result.iterrows():
            id = row['id']
            pnt_id = row['pnt_id']
            datum2 = row['datum']
            meting = row['meting']
            sat_id = row['sat_id']
            metingentijdelijklijstje.append([id, pnt_id, datum2, meting, sat_id])
    # deze dataframe zorgt dat de data bruikbaar is voor de volgende toepassingen
    dfpntidmeting = pd.DataFrame(metingentijdelijklijstje, columns=['id', 'pnt_id', 'datum', 'meting', 'sat_id'])
    return dfpntidmeting


def getmetingen(df):
    # Gebruikt het dataframe die aangemaakt is door de functie meetpuntenkoppelen
    engine = create_engine('postgresql://postgres:Welkom01!@10.30.1.10:5432/POC')
    templist = []
    ids = "', '".join(df['pnt_id'])
    select_query = """select * from meting where pnt_id in ('""" + ids + """')"""
    result = pd.read_sql_query(select_query, engine)
    for index, row in result.iterrows():
        id = row['id']
        pnt_id = row['pnt_id']
        datum2 = row['datum']
        meting = row['meting']
        sat_id = row['sat_id']
        templist.append([id, pnt_id, datum2, meting, sat_id])
    return pd.DataFrame(templist, columns=['id', 'pnt_id', 'datum', 'meting', 'sat_id'])


df = allesineen(355, 50)

df['datum'] = pd.to_datetime(df['datum'])
df['sat_id'] = df['sat_id'].astype('int')
df = df.sort_values(by='datum')
df['maand'] = pd.to_datetime(df['datum']).dt.strftime('%m')
df['maand'] = df['maand'].astype('int')
df['date_ordinal'] = pd.to_datetime(df['datum']).apply(lambda date: date.toordinal())
# df['date_ordinal']= df['date_ordinal']/4380
df.info()

df1 = df.loc[df['sat_id'] == 1]
df2 = df.loc[df['sat_id'] == 2]
df3 = df.loc[df['sat_id'] == 5]
df4 = df.loc[df['sat_id'] == 6]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=77)
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(x_train, y_train)
# Plot outputs
x = np.array(df1['date_ordinal']).reshape((-1, 1))
y = np.array(y_predict)
plt.scatter(x, y)
lm = LinearRegression()
model = lm.fit(x_train, y_train)
Coefficients = lm.coef_
Intercept = lm.intercept_
y_predict = lm.predict(x_test)
lm.fit(x_test, y_test)
plt.plot(x_test, y_predict, color='green')

lm = LinearRegression()
model = lm.fit(x_train, y_train)
Coefficients = lm.coef_
Intercept = lm.intercept_
y_predict = lm.predict(x_test)


def Lineaire_Regressie(a, b):
    df = allesineen(a, b)
    df['datum'] = pd.to_datetime(df['datum'])
    df['sat_id'] = df['sat_id'].astype('int')
    df = df.sort_values(by='datum')
    df['maand'] = pd.to_datetime(df['datum']).dt.strftime('%m')
    df['maand'] = df['maand'].astype('int')
    df['date_ordinal'] = pd.to_datetime(df['datum']).apply(lambda date: date.toordinal())
    df1 = df.loc[df['sat_id'] == 1]
    df2 = df.loc[df['sat_id'] == 2]
    df3 = df.loc[df['sat_id'] == 5]
    df4 = df.loc[df['sat_id'] == 6]

    lm = LinearRegression()

    x = np.array(df1['date_ordinal']).reshape((-1, 1))
    y = np.array(y_predict)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=77)
    y_predict = lm.predict(x_test)
    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(x_train, y_train)
    # Plot outputs

    plt.scatter(x, y)

    lm.fit(x_test, y_test)
    plt.plot(x_test, y_predict, color='green')


Lineaire_Regressie(355, 100)
