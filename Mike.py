import pandas as pd
import matplotlib.pyplot as plt

def GradenNaarMeters(meters):
   graden=(meters/30.92)/3600
   return graden

def puntenverzamelaar(puntfile,meters):
    #laad de punten file in
    puntenfile = pd.read_csv(puntfile)
    # id file
    idfile = []
    for row in puntenfile:
        maxlon = row('pnt_lon') + GradenNaarMeters(meters)
        minlon = row('pnt_lon') - GradenNaarMeters(meters)
        maxlan = row('pnt_lat') + GradenNaarMeters(meters)
        minlan = row('pnt_lat') - GradenNaarMeters(meters)
        id= pnt_id
        idfile.append(id,maxlon,minlon,maxlan,minlan)
    return print(idfile)

#puntenverzamelaar('prov_overijssel_eindhoven_rsat2_asc_xf_v2_ds_hoge_punten.csv',50)
puntenfile = pd.read_csv('inactieve_putten - page 1 2.csv')
#for row in puntenfile:
#    print(row)
#print(puntenfile.head())
#pnt_id = puntenfile['pnt_id']
#print(puntenfile.dtypes)
#for row in puntenfile:
#    print(row)
inactieveputtendf= pd.read_csv('inactieve_putten - page 1 2.csv',sep=',',)

def puntenverzamelaar2 (dataset,meters):
    eindlist = list()
    for row in dataset:
        #id = puntenlijst.append(dataset.loc[:, 'pnt_id'])
        maxlon = eindlist.append(dataset.loc[:, 'pnt_lon'] + GradenNaarMeters(meters))
        minlon = eindlist.append(dataset.loc[:, 'pnt_lon'] - GradenNaarMeters(meters))
        maxlan = eindlist.append(dataset.loc[:, 'pnt_lat'] + GradenNaarMeters(meters))
        minlan = eindlist.append(dataset.loc[:, 'pnt_lat'] - GradenNaarMeters(meters))
    return print(eindlist)
print(puntenverzamelaar2(inactieveputtendf, 50))
#print(inactieveputtendf.head())
#print(dataset.loc[:, 'pnt_lat'] - GradenNaarMeters(meters))