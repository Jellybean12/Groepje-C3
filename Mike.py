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
lijstje = puntenverzamelaar(inactieveputtendf, 100)
print(lijstje)

puntenlist = pd.read_csv('prov_overijssel_eindhoven_rsat2_asc_xf_v2_ds_hoge_punten.csv')

punten = []

for index, row in puntenlist.iterrows():
    for lijstje_index, lijstje_row in lijstje.iterrows() :
        if row['pnt_lon'] <= lijstje_row['MaxLon'] and row['pnt_lon'] >= lijstje_row['MinLon'] and  row['pnt_lat'] <= lijstje_row['MaxLat'] and row['pnt_lat'] >= lijstje_row['MinLat'] :
            print(lijstje_row['Locatie'])
            print(row['pnt_id'])
            print(row['pnt_lon'])
            print(row['pnt_lat'])









