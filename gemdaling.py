import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import sqlite3

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


#print(meetpuntenkoppelen(sqldataset,inactieveputtendf, 1500000))
#def koppelmeetpuntenmetboorlocaties(datasetmeetpunten,datasetboorlocatie,radius,bestandsnaam,)
#    meetpuntenkoppelen(datasetmeetpunten,datasetboorlocatie,radius).to_csv(bestandsnaam'.csv',index=False)

test123 = pd.DataFrame({"pnt_lon":[6.85581],"pnt_lat":[52.35096],"Locatie":['N/A'],"Boring":["N/A"]})
boorlocatie = radiusbepaler(test123, 1000)
#print(boorlocatie.head())
puntid = meetpuntenkoppelen(sqldataset,test123,125)
print(puntid)

engine = create_engine('postgresql://postgres:Welkom01!@10.30.1.10:5432/POC')
query = "SELECT * FROM meting WHERE pnt_id IN 'L485027P138209' LIMIT 50"
df = pd.read_sql(query, engine)
print(df)



#def gemdaling():
#    engine = create_engine('postgresql://postgres:Welkom01!@10.30.1.10:5432/POC')
#    query = "SELECT * FROM meting WHERE pnt_id IN 'L485027P138209' LIMIT 50"
#    df = pd.read_sql(query, engine)
#    print(df)

#gemdeling()
    #if df.loc[df['datum'].between('2015-01-01', '2015-06-31', inclusive=False)]:


  #  aantal = len(df['meting'])
  #  meting = df['meting']
  #  totaal = meting.sum()
  #  gemiddelde = (totaal / aantal)
  #  print(gemiddelde)

