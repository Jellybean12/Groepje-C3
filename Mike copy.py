import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

#testdatafile
#inactieveputtendf= pd.read_csv('inactieve_putten - page 1 2.csv',sep=',')
#puntenlist = pd.read_csv('prov_overijssel_eindhoven_rsat2_asc_xf_v2_ds_hoge_punten.csv')

###########SQL stukje###########
engine = create_engine('postgresql://postgres:Welkom01!@10.30.1.10:5432/POC')
sqldataset = pd.read_sql_query('Select * From locatie',engine)
#print(sqldataset)

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

#########vana dit punt is er verandering in vergelijking met mike.py#########

#Dit is een tijdelijke work around voor niet schone data, dus punten waar je alleen de coordinaten hebt maar bijvoorbeeld niet de locatie en boornummer
grondwaterontrekkinggebied = pd.DataFrame({"pnt_lon":[6.85581],"pnt_lat":[52.35096],"Locatie":['N/A'],"Boring":["N/A"]})
#dit zijn de instellingen
datameetpunten = meetpuntenkoppelen(sqldataset,grondwaterontrekkinggebied,30)
print(datameetpunten)

#dit is de select query die alle meetpunten sorteerd op punt id
select_query = "select * from meting where pnt_id = "
#tijdelijk lijstje
metingentijdelijklijstje = []
#eerste for loop zorgt voor de raw data die daarna nog per row uitgezocht moet worden zodra de tweede for loop klaar is -
# dus per row gaat hij naar de volgende punt id en daar alle raw data van pakken
for id in datameetpunten['pnt_id']:
    id2 = "'" + id + "'"
    var = select_query + id2
    result = pd.read_sql_query(var,engine)
    for index, row in result.iterrows():
        id = row['id']
        pnt_id = row['pnt_id']
        datum2 = row['datum']
        meting = row['meting']
        sat_id = row['sat_id']
        metingentijdelijklijstje.append([id, pnt_id, datum2, meting, sat_id])
#deze dataframe zorgt dat de data bruikbaar is voor de volgende toepassingen
dfpntidmeting = pd.DataFrame(metingentijdelijklijstje,columns=['id','pnt_id','datum','meting','sat_id'])
print(dfpntidmeting)