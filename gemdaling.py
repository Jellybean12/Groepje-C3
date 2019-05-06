import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import sqlite3



def gemdaling():
    engine = create_engine('postgresql://postgres:Welkom01!@10.30.1.10:5432/POC')
    query = "SELECT * FROM meting WHERE pnt_id = 'L485027P138209' LIMIT 50"
    df = pd.read_sql(query, engine)
    #print(df['meting'].count())
    aantal = len(df['meting'])
    meting = df['meting']
    totaal = meting.sum()
    gemiddelde = (totaal / aantal)
    print(gemiddelde)