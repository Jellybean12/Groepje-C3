# De benodigde imports
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import sqlite3
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import datetime
from tqdm import tqdm

# Instelling voor het uitvoeren
desired_width=320

sqldataset = pd.read_sql_query("""SELECT * FROM pnt_locatie""", engine)
sqldatasetboor = pd.read_sql_query("""SELECT * FROM boor_locatie WHERE boor_id = '999'""", engine)

# meet punten koppelen uit mikes stuk halen in de master
datameetpunten = meetpuntenkoppelen(sqldataset,sqldatasetboor,3000)
print(datameetpunten)

from matplotlib.pyplot import figure
plt.figure(figsize=(50,50))
plt.scatter(datameetpunten['pnt_lon'], datameetpunten['pnt_lat'])
plt.show()

# DEze misschien ook van mike
def getmetingen(locatie, sat):
    #Gebruikt het dataframe die aangemaakt is door de functie meetpuntenkoppelen
    engine = create_engine('postgresql://postgres:Welkom01!@localhost/POC')
    templist = []
    #ids = "', '".join(df['pnt_id'])
    select_query = "select * from meting where pnt_id in (Select pnt_id from pnt_locatie where locatie = '"+str(locatie)+"') and sat_id = '"+str(sat)+"')"
    result = pd.read_sql_query(select_query,engine)
    for index, row in result.iterrows():
        id = row['id']
        pnt_id = row['pnt_id']
        datum2 = row['datum']
        meting = row['meting']
        sat_id = row['sat_id']
        templist.append([id, pnt_id, datum2, meting, sat_id])
    return pd.DataFrame(templist,columns=['id','pnt_id','datum','meting','sat_id'])



####### hier functies ook gebruiken van fien (per half jaar en zo) ##########

def reg_plot_all_pnt_meting(df, w, h):
    """Deze functie maakt een regressie plot van een DataFrame. Gebruikende datum_ordinal als x en meting als y"""
    df['date_ordinal'] = pd.to_datetime(df['datum']).apply(lambda date: date.toordinal())
    plt.figure(figsize=(w, h))
    ax = sns.regplot(
        data=df,
        x='date_ordinal',
        y='meting')
    ax.set_title(title)
    ax.set_xlabel('Datum')
    ax.set_ylabel('Gemiddelde daling in meters')
    ax.set_xticklabels(df['datum'].astype(str))


# functies om plot te maken
def line_plot_average_half_year(df, type):
    """Deze functie maakt een lijn plot van een DataFrame. Gebruik een df die aangemaakt is door de functie Gebruikende datum_ordinal als x en meting als y"""
    # data = per_unique_point_average_half_year(df)
    # plt.figure(figsize=(w,h))
    ax = sns.lineplot(
        data=df,
        x='halfjaar',
        y='gemiddelde',
        # legend=False,
        size=10)
    ax.set_xlabel('Datum per halfjaar')
    ax.set_ylabel('Gemiddelde daling in meters')
    ax.set_title(title)
    fig = ax.get_figure()
    fig.set_size_inches(16, 10)
    fig.savefig('C:\\Users\\Proof of Concept\\Pictures\\autonome_daling_vvdaarle_' + str(type) + '.png')

def line_plot_average_half_year(df, type):
    """Deze functie maakt een lijn plot van een DataFrame. Gebruik een df die aangemaakt is door de functie Gebruikende datum_ordinal als x en meting als y"""
    #data = per_unique_point_average_half_year(df)
    #plt.figure(figsize=(w,h))
    ax = sns.lineplot(
        data=df,
        x='halfjaar',
        y='gemiddelde',
        #legend=False,
        size=10)
    ax.set_xlabel('Datum per halfjaar')
    ax.set_ylabel('Gemiddelde daling in meters')
    ax.set_title(title)
    fig = ax.get_figure()
    fig.set_size_inches(16, 10)
    fig.savefig('C:\\Users\\Proof of Concept\\Pictures\\autonome_daling_vvdaarle_'+str(type)+'.png')

#Plot meting 4
def line_plot_average_half_year(df, locatie):
    """Deze functie maakt een lijn plot van een DataFrame. Gebruik een df die aangemaakt is door de functie Gebruikende datum_ordinal als x en meting als y"""
    #data = per_unique_point_average_half_year(df)
    #plt.figure(figsize=(w,h))
    title = 'Autonome daling '+str(locatie)+''
    ax = sns.lineplot(
        data=df,
        x='halfjaar',
        y='gemiddelde', legend=False, size=10)
    ax.set_xlabel('Datum per halfjaar')
    ax.set_ylabel('Gemiddelde meting in meters')
    ax.set_title(title)
    fig = ax.get_figure()
    fig.set_size_inches(16, 10)
    fig.savefig('C:\\Users\\Proof of Concept\\Pictures\\autonome_daling_ '+str(locatie)+'.png')

#Plot meting 10
def line_plot_average_half_year(df):
    """Deze functie maakt een lijn plot van een DataFrame. Gebruik een df die aangemaakt is door de functie Gebruikende datum_ordinal als x en meting als y"""
    #data = per_unique_point_average_half_year(df)
    #plt.figure(figsize=(w,h))
    ax = sns.lineplot(
        data=df,
        x='halfjaar',
        y='gemiddelde',
        #Legend=False,
        size=10)
    ax.set_xlabel('Datum per halfjaar')
    ax.set_ylabel('Gemiddelde daling in meters')
    ax.set_title(title)
    fig = ax.get_figure()
    fig.set_size_inches(16, 10)
    fig.savefig('C:\\Users\\Proof of Concept\\Pictures\\autonome_daling_vvdaarle_XFHPD.png')

def getmetinggrond():
    #Gebruikt het dataframe die aangemaakt is door de functie meetpuntenkoppelen
    engine = create_engine('postgresql://postgres:Welkom01!@localhost/POC')
    templist = []
    #ids = "', '".join(df['pnt_id'])
    select_query = "select * from meting where pnt_id in (Select pnt_id from temp_locatie_vriezenveen) AND sat_id = '"+str(satid)+"'"
    result = pd.read_sql_query(select_query,engine)
    for index, row in result.iterrows():
        id = row['id']
        pnt_id = row['pnt_id']
        datum2 = row['datum']
        meting = row['meting']
        sat_id = row['sat_id']
        templist.append([id, pnt_id, datum2, meting, sat_id])
    return pd.DataFrame(templist,columns=['id','pnt_id','datum','meting','sat_id'])