#In dit bestand staan alle functies
#Modules importeren
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import re

def bestand(bestandsnaam):
    #Deze funtie verwijderd de lage streepjes uit een bestandsnaam
    nieuwbestand = bestandsnaam.replace("_", " ")
    return nieuwbestand

def get_type(invoer):
    """Deze functie bepaalt het type(HPA,HPD etc) op basis van de invoer"""
    #Als ascending, ds en hoge in invoer zit, return HDA
    if (' env ' in invoer or ' v3 ' in invoer):
        if ' ds ' in invoer:
            return 'DD'
        elif ' ps ' in invoer:
            return 'PD'
        else :
            raise ValueError('Geen goede bestandsnaam!')
    elif ' asc ' in invoer:
        if ' ds ' in invoer:
            if ' hoge ' in invoer:
                return 'HDA'
            #Als dit niet zo is, return LDA
            elif ' lage ' in invoer:
                return 'LDA'
            else :
                raise ValueError('Geen goede bestandsnaam!')
        #Als er hoge, ps en asc inzit, return HPA
        elif ' hoge ' in invoer:
            return 'HPA'
        elif ' lage ' in invoer:
            return 'LPA'
        else :
            raise ValueError('Geen goede bestandsnaam!')
    #Als er ds, hoge en andere lage inzit, return HDD of LDD
    elif ' ds ' in invoer:
        if ' hoge ' in invoer:
            return 'HDD'
        elif ' lage ' in invoer:
            return 'LDD'
        else :
            raise ValueError('Geen goede bestandsnaam!')
    #Als er hoge inzit, return HPD
    elif ' hoge ' in invoer:
        return 'HPD'
    #anders, return LPD
    elif ' lage ' in invoer:
        return 'LPD'
    else:
        raise ValueError('Geen goede bestandsnaam!')


def get_satalliet(invoer):
    #Als rsat2 in de naam zit, return rsatxf
    if 'rsat2' in invoer:
        return 'rsatxf'
    #Als rsat3 in de naam zit, return rsat3
    elif 'rsat3' in invoer:
        return 'rsat3'
    #Anders is het automatisch env
    else:
        return 'env'

def radiusbepaler (dataset,meters):
    #radiusbepaler zorgt ervoor dat er een dataframe gevult met de boorlocaties en de desbetreffende radius in meters wordt gereturned
    endlist= pd.DataFrame()
    def GradenNaarMeters(meters):
        graden = (meters / 30.92) / 3600
        return graden
    for row in dataset:
        boorid = endlist["BoorID"] = dataset.loc[:, 'Boring']
        locatie = endlist["Locatie"] = dataset.loc[:, 'Locatie']
        maxlon = endlist["MaxLon"] = dataset.loc[:, 'pnt_lon'] + GradenNaarMeters(meters)
        minlon = endlist["MinLon"] = dataset.loc[:, 'pnt_lon'] - GradenNaarMeters(meters)
        maxlat = endlist["MaxLat"] = dataset.loc[:, 'pnt_lat'] + GradenNaarMeters(meters)
        minlat = endlist["MinLat"] = dataset.loc[:, 'pnt_lat'] - GradenNaarMeters(meters)
    return endlist

def schoon(naam):
    data = pd.read_csv(naam)
    data = data[['pnt_id', 'pnt_lat', 'pnt_lon']]
    return data

def chunker(seq, size):
    # from http://stackoverflow.com/a/434328
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def insert_with_progress(df):
    #maak connectie met database
    con = create_engine('postgresql://postgres:Welkom01!@localhost:5432/POC')
    # set chunksize
    chunksize = int(len(df) / 10000)
    with tqdm(total=len(df)) as pbar:
        for i, cdf in enumerate(chunker(df, chunksize)):
            # chunked df toevoegen aan database in tabel meting
            cdf.to_sql('meting', con=con, if_exists='append', index=False)
            pbar.update(chunksize)


def convert_dataframe_datums(file) :
    # 1. Begin met een gewone dataframe van de csv
    original_df = pd.read_csv(file)
    # 2. Replace de d_ in de datum kolommen
    original_df.columns = original_df.columns.str.replace('d_', '')
    # 3. Maak een temp dataframe met alleen de datum kolommen
    temp = original_df.iloc[:,9:-2]
    # 4. Verander de namen van de datum kolommen naar date
    temp.columns = pd.to_datetime(temp.columns).date
    # 5. Voeg de 'pnt_id' kolom van de oorspronkelijke csv toe aan de temp
    temp['pnt_id'] = original_df['pnt_id']
    # 6. Maak van de temp een dataframe waarbij de datum kolommen values worden
    temp = temp.set_index('pnt_id').stack().reset_index()
    # 7. Verander de kolom namen van de temp dataframe
    result = temp.rename(columns={'level_1':'datum', 0:'meting'})
    # 8. Selecteer het id van de betreffende satelliet
    satname = get_satelliet(file)
    sattype = get_type(file)
    query = "SELECT sat_id FROM satelliet WHERE sat_naam = '" + satname + "' AND type ='" + sattype +"'"
    sat_id = pd.read_sql_query(query, engine).iloc[0, 0]
    # 9. Maak een nieuwe kolom 'sat_id' met het betreffende id en voeg die toe aan de dataframe
    result['sat_id'] = sat_id
    return result

def convert_all_files(files_list) :
    dataframe_collection = {}
    for file in files_list :
        # Hier wordt de convert functie aangeroepen en een dataframe is gemaakt
        df = convert_dataframe_datums(file)
        # Hier moet nog komen dat de df dan wordt toegevoegd aan de database
        insert_with_progress(df)

def meetpuntenkoppelen(datasetmeetpunten,datasetboorlocatie,radius):
    #deze functie zorgt ervoor dat de meetpunten gekoppeld worden aan een boorlocatie zodra die binnen de opgegeven radius zit
    punten = []
    meting = radiusbepaler(datasetboorlocatie,radius)
    for index, row in datasetmeetpunten.iterrows():
        for lijstje_index, lijstje_row in meting.iterrows() :
            if row['pnt_lon'] <= lijstje_row['MaxLon'] and row['pnt_lon'] >= lijstje_row['MinLon'] and  row['pnt_lat'] <= lijstje_row['MaxLat'] and row['pnt_lat'] >= lijstje_row['MinLat'] :
                boorid = lijstje_row['BoorID']
                locatie = lijstje_row['Locatie']
                minlon = lijstje_row['MinLon']
                maxlon = lijstje_row['MaxLon']
                minlat = lijstje_row['MinLat']
                maxlat = lijstje_row['MaxLat']
                pnt_id = row['pnt_id']
                pnt_lon = row['pnt_lon']
                pnt_lat = row['pnt_lat']
                punten.append([boorid,locatie,minlon,maxlon,minlat,maxlat,pnt_id,pnt_lon,pnt_lat])
    return pd.DataFrame(punten,columns=['boorid','locatie','minlon','maxlon','minlat','maxlat','pnt_id','pnt_lon','pnt_lat'])


#print(meetpuntenkoppelen(sqldataset,inactieveputtendf, 1500000))
def koppelmeetpuntenmetboorlocaties(datasetmeetpunten,datasetboorlocatie,radius,bestandsnaam,)
    meetpuntenkoppelen(datasetmeetpunten,datasetboorlocatie,radius).to_csv((bestandsnaam'.csv',index=False)