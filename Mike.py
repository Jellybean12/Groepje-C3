import pandas as pd
import matplotlib.pyplot as plt

#testdatafile
inactieveputtendf= pd.read_csv('inactieve_putten - page 1 2.csv',sep=',')
puntenlist = pd.read_csv('prov_overijssel_eindhoven_rsat2_asc_xf_v2_ds_hoge_punten.csv')

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


print(meetpuntenkoppelen(puntenlist,inactieveputtendf, 150))
#meetpuntenkoppelen().to_csv('test.csv',index=False)