import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from scipy.stats import linregress
from tqdm import tqdm

url = 'postgresql://postgres:Welkom01!@10.30.1.10:5432/POC'


def create_ri_df(sat_id):
    """Berekent de helling/daling in millimeter per jaar van elk pnt_id. Gebruikt de pnt_id's van het sat_id dat mee is gegeven."""
    templist_ri = []
    query = """select * from meting where sat_id = '""" + sat_id + """'"""
    sqlchunks = pd.read_sql(query, con=url, chunksize=1000)

    sqldataset = pd.DataFrame()
    for chunk in tqdm(sqlchunks):
        sqldataset = pd.concat([sqldataset, chunk])

    for i in sqldataset.pnt_id.unique():
        df_per_pnt = sqldataset.loc[sqldataset['pnt_id'] == i]
        df_per_pnt['date_ordinal'] = pd.to_datetime(df_per_pnt['datum']).apply(lambda date: date.toordinal())
        x = df_per_pnt['date_ordinal']
        y = df_per_pnt['meting']
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        slopeinmeters = slope * 1000
        perjaar = slopeinmeters * 365
        templist_ri.append([i, perjaar])
    return pd.DataFrame(templist_ri, columns=['pnt_id', 'pnt_ri'])


sat10_ri = create_ri_df('10')
