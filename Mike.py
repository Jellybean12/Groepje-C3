import pandas as pd
import matplotlib.pyplot as plt

#datafile
inactieveputtendf= pd.read_csv('inactieve_putten - page 1 2.csv',sep=',',)

def GradenNaarMeters(meters):
   graden=(meters/30.92)/3600
   return graden

#functie voor het verzamelen van punten
def puntenverzamelaar2 (dataset,meters):
    eindlist = list()
    #een for loop zodat alle rows in een dataframe wordt gebruikt om meer
    for row in dataset:
        id = eindlist.append(dataset.loc[:, 'Locatie'])
        maxlon = eindlist.append(dataset.loc[:, 'pnt_lon'] + GradenNaarMeters(meters))
        minlon = eindlist.append(dataset.loc[:, 'pnt_lon'] - GradenNaarMeters(meters))
        maxlan = eindlist.append(dataset.loc[:, 'pnt_lat'] + GradenNaarMeters(meters))
        minlan = eindlist.append(dataset.loc[:, 'pnt_lat'] - GradenNaarMeters(meters))
    return print(eindlist)
print(puntenverzamelaar2(inactieveputtendf, 50))