import pandas as pd
import matplotlib.pyplot as plt

#datafile
inactieveputtendf= pd.read_csv('inactieve_putten - page 1 2.csv',sep=',',)

def GradenNaarMeters(meters):
   graden=(meters/30.92)/3600
   return graden

#functie voor het verzamelen van punten


#if statement om te kijken of een dieptemetingpunt in range is met de zoutcaverne
punten = []
#for row in eindlist:
#    if pnt_lon in range(minlon,maxlon) and pnt_lat in range(minlat,maxlat):
#    punten.append(pnt_id)

###############################
inactieveputtendf= pd.read_csv('inactieve_putten - page 1 2.csv',sep=',',)
#print(inactieveputtendf)
#def puntenverzamelaar2 (dataset,meters):
#   locatie = []
#   maxlon = []
#   minlon= []
#  maxlat= []
#   minlat= []
   #een for loop zodat alle rows in een dataframe wordt gebruikt om meer
#   for row in dataset:
#       locatie.append(dataset.loc[:, 'Locatie'])
#       maxlon.append(dataset.loc[:, 'pnt_lon'] + GradenNaarMeters(meters))
#       minlon.append(dataset.loc[:, 'pnt_lon'] - GradenNaarMeters(meters))
 #      maxlat.append(dataset.loc[:, 'pnt_lat'] + GradenNaarMeters(meters))
#       minlat.append(dataset.loc[:, 'pnt_lat'] - GradenNaarMeters(meters))

#   eindlist= pd.DataFrame(columns=[["Locatie","MaxLat","MinLat","MaxLon","MinLon"]])

#for row in
#   eindlist["Locatie"]=locatie
#   eindlist["MaxLat"]=maxlat
#   eindlist["MinLat"]=minlat
#   eindlist["MaxLon"]=maxlon
#   eindlist["MinLon"]=minlon


#   return pd.DataFrame(eindlist)




def puntenverzamelaar2 (dataset,meters):
    #eindlist= []
    eindlist= pd.read_csv('csv boor.csv')
    #een for loop zodat alle rows in een dataframe wordt gebruikt om meer
    for row in dataset:
        eindlist["BoorID"] = dataset.loc[:, 'Boring']
        eindlist["Locatie"] = dataset.loc[:, 'Locatie']
        eindlist["MaxLon"] = dataset.loc[:, 'pnt_lon'] + GradenNaarMeters(meters)
   # maxlon = eindlist.append({'MaxLon': dataset.loc[:, 'pnt_lon'] + GradenNaarMeters(meters)})
        eindlist["MinLon"] = dataset.loc[:, 'pnt_lon'] - GradenNaarMeters(meters)
        eindlist["MaxLat"] = dataset.loc[:, 'pnt_lat'] + GradenNaarMeters(meters)
        eindlist["MinLat"] = dataset.loc[:, 'pnt_lat'] - GradenNaarMeters(meters)
    return print(eindlist)
print(puntenverzamelaar2(inactieveputtendf, 50))








