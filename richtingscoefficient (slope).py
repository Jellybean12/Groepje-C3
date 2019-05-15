import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

def richtingscoefficient(pnt, dfmeting = 0):
    if dfmeting == 0:
        def create_dataframe_from_query(url, query):
            """Maakt een connectie met een database met de meegegeven url. Met de query wordt een dataframe gemaakt."""
            engine = create_engine(url)
            df = pd.read_sql(query, engine)
            return df

        url = 'postgresql://postgres:Welkom01!@10.30.1.10:5432/POC'
        query = """select * from meting where pnt_id in ('""" + pnt + """')"""
        df = create_dataframe_from_query(url, query)
    if dfmeting != 0:
        df = dfmeting
    df['date_ordinal'] = pd.to_datetime(df['datum']).apply(lambda date: date.toordinal())
    #print(df.head())
    df.plot(x='date_ordinal', y='meting')

    #### richtingscoefficient gedeelte ####
    # (X*Y).mean(axis=1) - X.mean()*Y.mean(axis=1)) / ((X**2).mean() - (X.mean())**2)
    x = df['date_ordinal']
    y = df['meting']
    from scipy.stats import linregress
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    slopeinmeters = slope * 1000
    #print(slopeinmeters * 365)
    # print('de verzaking is: ',slopeinmeters,'CM')
    #plt.plot(x, y, 'o', label='original data')
    #plt.plot(x, intercept + slope * x, 'r', label='fitted line')
    #plt.legend()
    return print('De gemiddelde stijging/daling van punt ',pnt,' is : ',slopeinmeters*365,'mm per jaar  ')


print(richtingscoefficient('L346887P7846'))
