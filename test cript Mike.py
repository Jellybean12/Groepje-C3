import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:Welkom01!@10.30.1.10:5432/POC')
sqldataset2 = pd.read_sql_query("Select * From pnt_locatie WHERE pnt_id='L373252P179009' OR pnt_id='L373296P178121'", engine)
sqldataset3 = pd.read_sql_query("Select * From pnt_locatie WHERE pnt_id='L373252P179009' OR pnt_id='L373296P178121' OR pnt_id='L373415P178584'", engine)
datameetpunten = sqldataset2
datameetpuntengroot = sqldataset3


print('----------------------------')
print('klein')
print(datameetpunten)
print('----------------------------')
print('groot')
print(datameetpuntengroot)
print('----------------------------')

datameetpunten_merge = datameetpunten.append(datameetpuntengroot, ignore_index=True)

print('merge')
print(datameetpunten_merge)
print('----------------------------')

datameetpunten_merge = datameetpunten_merge.drop_duplicates(subset='pnt_id', keep=False)

print(datameetpunten_merge)