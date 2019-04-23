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
puntenfile = pd.read_csv('prov_overijssel_eindhoven_rsat2_asc_xf_v2_ds_hoge_punten.csv')
#for row in puntenfile:
#    print(row)
#print(puntenfile.head())
#pnt_id = puntenfile['pnt_id']
#print(puntenfile.dtypes)
#for row in puntenfile:
#    print(row)

def puntenverzamelaar2 (dataset):
    puntenlijst = list()
    for row in dataset:
        puntenlijst.append(dataset.loc[:,'pnt_id'])
        puntenlijst.append(dataset.loc[:,'pnt_lon'])
        puntenlijst.append(dataset.loc[:,'pnt_lon'])
        puntenlijst.append(dataset.loc[:,'pnt_lat'])
        puntenlijst.append(dataset.loc[:,'pnt_lat'])
    return(puntenlijst)

print(puntenverzamelaar2(puntenfile))
#print(puntenfile.loc[:,'pnt_id'])