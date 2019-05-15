#Dit is er nodig
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine

desired_width=320

pd.set_option('display.width', desired_width)

np.set_printoptions(linewidth=desired_width)

pd.set_option('display.max_columns',10)

#testdatafile
#inactieveputtendf= pd.read_csv('inactieve_putten - page 1 2.csv',sep=',')
#puntenlist = pd.read_csv('prov_overijssel_eindhoven_rsat2_asc_xf_v2_ds_hoge_punten.csv')
def allesineen(boorid, radiusinmeter, radiusgroot):
    ###########SQL stukje###########
    engine = create_engine('postgresql://postgres:Welkom01!@10.30.1.10:5432/POC')
    sqldataset = pd.read_sql_query('Select * From pnt_locatie', engine)
    sqldatasetboorquery = "Select * From boor_locatie where boor_id = "
    booridtostr = str(boorid)
    booridaddon = "'" + booridtostr + "'"
    booridcompletequery = sqldatasetboorquery + booridaddon
    sqldatasetboor = pd.read_sql_query(booridcompletequery, engine)
    #print('DEVINFO info van boorlocatie: ',sqldatasetboor)

    def radiusbepaler(dataset, meters,):
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
        #print('DEVINFO info max en minlon : ',endlist.head())
        return endlist

    # print(radiusbepaler(sqldatasetboor,100))

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
        returndata =  pd.DataFrame(punten, columns=['boorid', 'locatie', 'minlon', 'maxlon', 'minlat', 'maxlat', 'pnt_id', 'pnt_lon', 'pnt_lat'])
        #print('DEVINFO meetpuntenkopellen: ',returndata.head())
        return returndata
    print('25% done')
    def meetpuntenkoppelengroot(datasetmeetpunten, datasetboorlocatie, radiusinmetergroot):
        # deze functie zorgt ervoor dat de meetpunten gekoppeld worden aan een boorlocatie zodra die binnen de opgegeven radius zit
        punten = []
        meting = radiusbepaler(datasetboorlocatie, radiusgroot)
        for index, row in datasetmeetpunten.iterrows():
            for lijstje_index, lijstje_row in meting.iterrows():
                if row['pnt_lon'] <= lijstje_row['MaxLon'] and row['pnt_lon'] >= lijstje_row['MinLon'] and row[
                    'pnt_lat'] <= lijstje_row['MaxLat'] and row['pnt_lat'] >= lijstje_row['MinLat']:
                    boorid = lijstje_row['BoorID']
                    locatie = lijstje_row['Locatie']
                    minlongroot = lijstje_row['MinLon']
                    maxlongroot = lijstje_row['MaxLon']
                    minlatgroot = lijstje_row['MinLat']
                    maxlatgroot = lijstje_row['MaxLat']
                    pnt_id = row['pnt_id']
                    pnt_lon = row['pnt_lon']
                    pnt_lat = row['pnt_lat']
                    punten.append([boorid, locatie, minlongroot, maxlongroot, minlatgroot, maxlatgroot, pnt_id, pnt_lon, pnt_lat])
        returndata =  pd.DataFrame(punten, columns=['boorid', 'locatie', 'minlongroot', 'maxlongroot', 'minlatgroot', 'maxlatgroot', 'pnt_id', 'pnt_lon', 'pnt_lat'])
        #print('DEVINFO meetpuntenkopellen radiusgroot: ',returndata)
        return returndata



    # Dit is een tijdelijke work around voor niet schone data, dus punten waar je alleen de coordinaten hebt maar bijvoorbeeld niet de locatie en boornummer
    grondwaterontrekkinggebied = pd.DataFrame(
        {"boor_lon": [6.85581], "boor_lat": [52.35096], "Locatie": ['N/A'], "boor_id": ["N/A"]})
    # dit zijn de instellingen
    datameetpunten = meetpuntenkoppelen(sqldataset, sqldatasetboor, radiusinmeter)
    datameetpuntengroot = meetpuntenkoppelengroot(sqldataset, sqldatasetboor, radiusgroot)
    #print('DEVINFO resulaten: ',datameetpunten.head())
    print('50% done')
#    for id in datameetpunten['pnt_id']:
#        if id in datameetpuntengroot['pnt_id']:
#            idvanpunt = "'" + id + "'"
#            datameetpuntengroot.drop([idvanpunt])
    #print('----------------------------')
    #print('klein')
    #print(datameetpunten)
    #print('----------------------------')
    #print('groot')
    #print(datameetpuntengroot)
    #print('----------------------------')

    datameetpunten_merge = datameetpunten.append(datameetpuntengroot, ignore_index=True)

    #print('merge')
    #print(datameetpunten_merge)
    #print('----------------------------')

    datameetpunten_merge = datameetpunten_merge.drop_duplicates(subset='pnt_id', keep=False)

    #print(datameetpunten_merge)

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
    #print('DEVINFO meeting info: ',dfpntidmeting)
    dfpntidmeting = getmetingen(datameetpunten)
    dfpntidmetinggroot = getmetingen(datameetpunten_merge)
    print('75% done')
    def maxdaling():
        return (dfpntidmeting['meting'].min())

    def maxstijging():
        return (dfpntidmeting['meting'].max())

    def gemdaling():
        return (dfpntidmeting['meting'].mean())

    def maxdalinggroot():
        return (dfpntidmetinggroot['meting'].min())

    def maxstijginggroot():
        return (dfpntidmetinggroot['meting'].max())

    def gemdalinggroot():
        return (dfpntidmetinggroot['meting'].mean())
    print('100% done')
    return print('maxdaling: ', maxdaling(), 'Meter ', 'maxstijging: ', maxstijging(), 'Meter ', 'gemdaling: ', gemdaling(),
          'Meter',' maxdaling van het omliggende gebied: ', maxdalinggroot(), 'Meter ', 'maxstijging van het omliggende gebied: ', maxstijginggroot(), 'Meter ', 'gemdaling van het omliggende gebied: ', gemdalinggroot(),
          'Meter')

allesineen(358, 100, 200)