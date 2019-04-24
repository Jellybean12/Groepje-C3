import pandas as pd
import matplotlib.pyplot as plt

#datafile
inactieveputtendf= pd.read_csv('inactieve_putten - page 1 2.csv',sep=',',)

def GradenNaarMeters(meters):
   graden=(meters/30.92)/3600
   return graden

#functie voor het verzamelen van punten
def puntenverzamelaar2 (dataset,meters):
    eindlist= []
    #een for loop zodat alle rows in een dataframe wordt gebruikt om meer
    #for row in dataset:
        #boorid = eindlist["BoorID"].append(dataset.loc[:, 'Boring'])
       #locatie = eindlist["Locatie"].append(dataset.loc[:, 'Locatie'])
        #maxlon = eindlist.append({"MaxLon" : (dataset.loc[:, 'pnt_lon'] + GradenNaarMeters(meters)})
    maxlon = eindlist.append({'MaxLon': dataset.loc[:, 'pnt_lon'] + GradenNaarMeters(meters)})
        #minlon = eindlist["MinLon"].append(dataset.loc[:, 'pnt_lon'] - GradenNaarMeters(meters))
        #maxlat = eindlist["MaxLat"].append(dataset.loc[:, 'pnt_lat'] + GradenNaarMeters(meters))
        #minlat = eindlist["MinLat"].append(dataset.loc[:, 'pnt_lat'] - GradenNaarMeters(meters))
    return print(eindlist)
#print(puntenverzamelaar2(inactieveputtendf, 50))
#if statement om te kijken of een dieptemetingpunt in range is met de zoutcaverne
punten = []
#for row in eindlist:
#    if pnt_lon in range(minlon,maxlon) and pnt_lat in range(minlat,maxlat):
#    punten.append(pnt_id)

###############################
inactieveputtendf= pd.read_csv('inactieve_putten - page 1 2.csv',sep=',',)

def puntenverzamelaar2 (dataset,meters):
   locatie = []
   maxlon = []
   minlon= []
   maxlat= []
   minlat= []
   #een for loop zodat alle rows in een dataframe wordt gebruikt om meer
   for row in dataset:
       locatie.append(dataset.loc[:, 'Locatie'])
       maxlon.append(dataset.loc[:, 'pnt_lon'] + GradenNaarMeters(meters))
       minlon.append(dataset.loc[:, 'pnt_lon'] - GradenNaarMeters(meters))
       maxlat.append(dataset.loc[:, 'pnt_lat'] + GradenNaarMeters(meters))
       minlat.append(dataset.loc[:, 'pnt_lat'] - GradenNaarMeters(meters))

   eindlist= pd.DataFrame(columns=[["Locatie","MaxLat","MinLat","MaxLon","MinLon"]])

for row in
   eindlist["Locatie"]=locatie
   eindlist["MaxLat"]=maxlat
   eindlist["MinLat"]=minlat
   eindlist["MaxLon"]=maxlon
   eindlist["MinLon"]=minlon


   return pd.DataFrame(eindlist)