import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from scipy.stats import linregress
from tqdm import tqdm

url = 'postgresql://postgres:Welkom01!@localhost:5432/POC'

def insert_with_progress(df):
    # set chunksize
    chunksize = int(len(df) / 100)
    with tqdm(total=len(df)) as pbar:
        for i, cdf in enumerate(chunker(df, chunksize)):
            # chunked df toevoegen aan database
            cdf.to_sql('temp_locatie_ri', con=url, if_exists='append', index=False)
            pbar.update(chunksize)

def create_ri_df(sat_id):
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
insert_with_progress(sat10_ri)