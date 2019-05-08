import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:Welkom01!@10.30.1.10:5432/POC')
query = "SELECT * FROM meting WHERE pnt_id = 'L485027P138209' LIMIT 50"
df = pd.read_sql(query, engine)
print(df)