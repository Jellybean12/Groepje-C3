import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:Welkom01!@10.30.1.10:5432/POC')
sqldataset = pd.read_sql_query('Select * From pnt_locatie', engine)
sqldataset2 = pd.read_sql_query("Select * From pnt_locatie WHERE pnt_id='L373252P179009' OR pnt_id='L373296P178121'", engine)
sqldataset3 = pd.read_sql_query("Select * From pnt_locatie WHERE pnt_id='L373252P179009' OR pnt_id='L373296P178121' OR pnt_id='L373415P178584'", engine)
datameetpunten = sqldataset2
datameetpuntengroot = sqldataset3
#for id in datameetpunten['pnt_id']:
#    print(id)
#    print(datameetpuntengroot['pnt_id'])
#    idvanpunt = "'" + id + "'"
#    print(idvanpunt)
#    print('test')
#    datameetpuntengroot.drop(id, inplace = True)

cond = datameetpuntengroot['pnt_id'].isin(datameetpunten['pnt_id']) == True
datameetpuntengroot.drop(datameetpunten[cond].index, inplace = True)

print(datameetpuntengroot)