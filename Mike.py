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
    return print(eindlist)
lijstje = puntenverzamelaar(inactieveputtendf, 50)
print(lijstje)

puntenlist = pd.read_csv('prov_overijssel_eindhoven_rsat2_asc_xf_v2_ds_hoge_punten.csv')
punten = []
for row in puntenlist:
    if puntenlist['pnt_lon'] in range(lijstje['MinLon'], lijstje['MaxLon']) and puntenlist['pnt_lat'] in range(lijstje['MinLat'], lijstje['MaxLat']):
        punten.append(puntenlist['pnt_id'])








