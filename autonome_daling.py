import pandas as pd
from sqlalchemy import create_engine
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import gemiddelde_metingen as gem_met

def get_metingen(satid):
    """Met de functie getmetingen wordt er een select statement uitgevoerd met het geselecteerde sat_id, deze functie is gebruikt
    voor de nulmeting vriezenveen/daarle. Deze functie haalt alle data op uit de meting tabel, deze kan evt worden aangepast voor de benodigde data"""
    engine = create_engine('postgresql://postgres:Welkom01!@localhost/POC')
    templist = []
    select_query = "select * from meting where pnt_id in (Select pnt_id from temp_locatie_vriezenveen) AND sat_id = '" + str(
        satid) + "'"
    result = pd.read_sql_query(select_query, engine)
    for index, row in result.iterrows():
        id = row['id']
        pnt_id = row['pnt_id']
        datum2 = row['datum']
        meting = row['meting']
        sat_id = row['sat_id']
        templist.append([id, pnt_id, datum2, meting, sat_id])
    return pd.DataFrame(templist, columns=['id', 'pnt_id', 'datum', 'meting', 'sat_id'])


def line_plot_average_half_year(df, locatie):                                                                                                                            
    """Deze functie maakt een lijn plot van een DataFrame. Gebruik een df die aangemaakt is door de functie Gebruikende datum_ordinal als x en meting als y"""      
    #data = per_unique_point_average_half_year(df)                                                                                                                   
    title = 'Autonome daling '+str(locatie)+''
    ax = sns.lineplot(                                                                                                                                              
        data=df,                                                                                                                                                  
        x='halfjaar',                                                                                                                                               
        y='gemiddelde',
        size=10)                                                                                                                                             
    ax.set_xlabel('Datum per halfjaar')                                                                                                                             
    ax.set_ylabel('Gemiddelde meting in meters')                                                                                                                    
    ax.set_title(title)    
    fig = ax.get_figure()
    fig.set_size_inches(16, 10)
    plt.show()

url = 'postgresql://postgres:Welkom01!@10.30.1.10:5432/POC'
query = """SELECT * FROM meting WHERE pnt_id IN (SELECT pnt_id FROM pnt_locatie WHERE locatie = 'Hammerflier' LIMIT 100)"""
df = gem_met.create_dataframe_from_query(url, query)

new_df = gem_met.per_unique_point_average_half_year(df)

line_plot_average_half_year(new_df, 'Hammerflier LIMIT 100')




