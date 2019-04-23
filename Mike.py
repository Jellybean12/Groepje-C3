import pandas as pd
import matplotlib.pyplot as plt
def puntenverzamelaar(puntfile,naam):
    #laad de punten file in
    puntenfile = pd.read_csv(puntfile)
    # id file
    idfile = pd.dataframe()
    idfile['naam','closest_point_id'] = match.append(lambda row: find_point(row['pnt_lat'], row['pnt_lon']), axis=1)