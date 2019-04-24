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
        eindlist["BoorID"] = dataset.loc[:, 'Boring']
        eindlist["Locatie"] = dataset.loc[:, 'Locatie']
        eindlist["MaxLon"] = dataset.loc[:, 'pnt_lon'] + GradenNaarMeters(meters)
        eindlist["MinLon"] = dataset.loc[:, 'pnt_lon'] - GradenNaarMeters(meters)
        eindlist["MaxLat"] = dataset.loc[:, 'pnt_lat'] + GradenNaarMeters(meters)
        eindlist["MinLat"] = dataset.loc[:, 'pnt_lat'] - GradenNaarMeters(meters)
    return print(eindlist)
print(puntenverzamelaar(inactieveputtendf, 50))








