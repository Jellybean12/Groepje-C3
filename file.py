import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:Welkom01!@10.30.1.10:5432/POC')
#sqldataset = pd.read_sql_query('Select * From pnt_locatie', engine)
sqldatasetboorquery = "Select * From boor_locatie where boor_id = "
boorid2 = str(355)
booridaddon = "'" + boorid2 + "'"
print(booridaddon)
booridcompletequery = sqldatasetboorquery + booridaddon
sqldatasetboor = pd.read_sql_query(booridcompletequery, engine)
print(sqldatasetboor)