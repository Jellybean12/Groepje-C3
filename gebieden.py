import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import ExcelWriter
from pandas import ExcelFile

#Functie voor het opschonen van de data
def schoon(naam):
    data = pd.read_csv(naam)
    data = data[['pnt_id', 'pnt_lat', 'pnt_lon']]
    return data

#Functie aanroepen met csv bestand
voorbeeld = schoon('prov_overijssel_groningen_rsat2_asc_xf_v2_ds_lage_punten.csv')

#Condities aangeven
conditie = [
    #Engelse Werk
    (voorbeeld['pnt_lat'] >= 52.46) & (voorbeeld['pnt_lat'] <= 52.54) & (voorbeeld['pnt_lon'] >= 6.0) & (voorbeeld['pnt_lon'] <= 6.2),
    #Hammerflier
    (voorbeeld['pnt_lat'] >= 52.44) & (voorbeeld['pnt_lat'] <= 52.5) & (voorbeeld['pnt_lon'] >= 6.5) & (voorbeeld['pnt_lon'] <= 6.7),
    #Manderveen
    (voorbeeld['pnt_lat'] >= 52.42) & (voorbeeld['pnt_lat'] <= 52.48) & (voorbeeld['pnt_lon'] >= 6.7) & (voorbeeld['pnt_lon'] <= 6.9),
    #Wierden
    (voorbeeld['pnt_lat'] >= 52.32) & (voorbeeld['pnt_lat'] <= 52.41) & (voorbeeld['pnt_lon'] >= 6.5) & (voorbeeld['pnt_lon'] <= 6.7),
    #Hasselo
    (voorbeeld['pnt_lat'] >= 52.28) & (voorbeeld['pnt_lat'] <= 52.32) & (voorbeeld['pnt_lon'] >= 6.7) & (voorbeeld['pnt_lon'] <= 6.9),
    #Weerselo
    (voorbeeld['pnt_lat'] >= 52.32) & (voorbeeld['pnt_lat'] <= 52.38) & (voorbeeld['pnt_lon'] >= 6.8) & (voorbeeld['pnt_lon'] <= 6.9),
    #Espelose broek
    (voorbeeld['pnt_lat'] >= 52.28) & (voorbeeld['pnt_lat'] <= 52.33) & (voorbeeld['pnt_lon'] >= 6.3) & (voorbeeld['pnt_lon'] <= 6.4),
    #Sint Jans Klooster
    (voorbeeld['pnt_lat'] >= 52.63) & (voorbeeld['pnt_lat'] <= 52.71) & (voorbeeld['pnt_lon'] >= 5.8) & (voorbeeld['pnt_lon'] <= 6.2),
    #Rodenmors
    (voorbeeld['pnt_lat'] >= 52.36) & (voorbeeld['pnt_lat'] <= 52.42) & (voorbeeld['pnt_lon'] >= 7.0) & (voorbeeld['pnt_lon'] <= 7.1),
    #Holten
    (voorbeeld['pnt_lat'] >= 52.24) & (voorbeeld['pnt_lat'] <= 52.33) & (voorbeeld['pnt_lon'] >= 6.4) & (voorbeeld['pnt_lon'] <= 6.5)
]

keuze = ['Engelse Werk', 'Hammerflier', 'Manderveen', 'Wierden', 'Hasselo', 'Weerselo', 'Espelose Broek', 'Holten', 'SintJansKlooster', 'Rodenmors']
voorbeeld['Gebied'] = np.select(conditie, keuze, default=0)

#Bestand opslaan als excel
#writer = ExcelWriter('eindhoven_rsat2_asc_xf_v2_ds_hoog_gebieden.xlsx')
#voorbeeld.to_excel(writer, 'Sheet1', index=False)
#writer.save()

#Scatterplot maken
scatter = sns.scatterplot(x='pnt_lon', y='pnt_lat', hue='Gebied', data=voorbeeld, legend='full')
plt.show(scatter)

hallo