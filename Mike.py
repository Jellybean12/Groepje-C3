import pandas as pd
import matplotlib.pyplot as plt

#datafile
inactieveputtendf= pd.read_csv('inactieve_putten - page 1 2.csv',sep=',',)

def GradenNaarMeters(meters):
   graden=(meters/30.92)/3600
   return graden

def puntenverzamelaar (dataset,meters):
    #eindlist= []
    eindlist= pd.read_csv('csv boor.csv')

    #een for loop zodat alle rows in een dataframe wordt gebruikt om meer
    for row in dataset:
        boorid = eindlist["BoorID"] = dataset.loc[:, 'Boring']
        locatie = eindlist["Locatie"] = dataset.loc[:, 'Locatie']
        maxlon = eindlist["MaxLon"] = dataset.loc[:, 'pnt_lon'] + GradenNaarMeters(meters)
        minlon = eindlist["MinLon"] = dataset.loc[:, 'pnt_lon'] - GradenNaarMeters(meters)
        maxlat = eindlist["MaxLat"] = dataset.loc[:, 'pnt_lat'] + GradenNaarMeters(meters)
        minlat = eindlist["MinLat"] = dataset.loc[:, 'pnt_lat'] - GradenNaarMeters(meters)
    return eindlist
lijstje = puntenverzamelaar(inactieveputtendf, 150)
print(lijstje)

puntenlist = pd.read_csv('prov_overijssel_eindhoven_rsat2_asc_xf_v2_ds_hoge_punten.csv')

def kopel():
    punten = []
    gekoppeldlijst = pd.read_csv('Punten gekoppeld aan zoutcaravens.csv')
    #gekoppeldlijst = pd.DataFrame(columns=["Locatie"])
    for index, row in puntenlist.iterrows():
        for lijstje_index, lijstje_row in lijstje.iterrows() :
            if row['pnt_lon'] <= lijstje_row['MaxLon'] and row['pnt_lon'] >= lijstje_row['MinLon'] and  row['pnt_lat'] <= lijstje_row['MaxLat'] and row['pnt_lat'] >= lijstje_row['MinLat'] :
                #print(lijstje_row['Locatie'])
                #print(lijstje_row['BoorID'])
                boorid = gekoppeldlijst["BoorID"] = lijstje_row['BoorID']
                locatie = gekoppeldlijst["Locatie"] = lijstje_row['Locatie']
                minlon = gekoppeldlijst["MinLon"] = lijstje_row['MinLon']
                maxlon = gekoppeldlijst["MaxLon"] = lijstje_row['MaxLon']
                minlat = gekoppeldlijst["MinLat"] = lijstje_row['MinLat']
                maxlat = gekoppeldlijst["MaxLat"] = lijstje_row['MaxLat']
                pnt_id = gekoppeldlijst["pnt_id"] = row['pnt_id']
                pnt_lon = row['pnt_lon']
                pnt_lat = row['pnt_lat']
                punten.append([boorid,locatie,minlon,maxlon,minlat,maxlat,pnt_id,pnt_lon,pnt_lat])
                #print(boorid)
    return print(pd.DataFrame(punten,columns=[boorid,locatie,minlon,maxlon,minlat,maxlat,pnt_id,pnt_lon,pnt_lat]))
kopel()