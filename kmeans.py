import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import seaborn as sns

def schoon(naam):
    data = pd.read_csv(naam)
    data = data[['pnt_lat', 'pnt_lon']]
    return data


data = schoon('prov_overijssel_eindhoven_rsat2_asc_xf_v2_ds_hoge_punten.csv')

def kmeans(data, clusters):
    model = KMeans(n_clusters=clusters)
    kmeansmodel = model.fit(data)
    data['cluster'] = kmeansmodel.labels_
    return data



#print(data.head)
voorbeeld = kmeans(schoon('prov_overijssel_eindhoven_rsat2_asc_xf_v2_ds_hoge_punten.csv'), 8)
data1 = voorbeeld.iloc[:, :18294]
data2 = voorbeeld.iloc[:, 18294:]

print(data2.info())

#scatter = sns.scatterplot(x='pnt_lon', y='pnt_lat', hue='cluster', data=data1, size='cluster', legend='full')
#plt.show(scatter)
#plt.show(var)
#plt.scatter(voorbeeld['pnt_lon'], voorbeeld['pnt_lat'], alpha=0.1)
#plt.show()

#print(data('prov_overijssel_eindhoven_rsat2_asc_xf_v2_ds_hoge_punten.csv'))
#scatterplot
#plt.scatter(df['pnt_lon'], df['pnt_lat'], alpha=0.1)