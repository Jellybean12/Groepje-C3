import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine


engine = create_engine('postgresql://postgres:Welkom01!@10.30.1.10:5432/POC')
stmt = "SELECT datum, meting FROM meting WHERE pnt_id = 'L460037P200100'"
result = pd.read_sql(stmt,engine)

result['datum'] = result['datum'].astype('str')
plt.scatter(x=result['datum'], y=result['meting'])
plt.show()


