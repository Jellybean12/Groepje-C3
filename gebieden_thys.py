import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from tqdm import tqdm

def chunker(seq, size):
    # from http://stackoverflow.com/a/434328
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def insert_with_progress(df):
    #maak connectie met database
    con = create_engine('postgresql://postgres:Welkom01!@10.30.1.10:5432/POC')
    # set chunksize
    chunksize = int(len(df) / 10000)
    with tqdm(total=len(df)) as pbar:
        for i, cdf in enumerate(chunker(df, chunksize)):
            # chunked df toevoegen aan database
            cdf.to_sql('pnt_locatie', con=con, if_exists='append', index=False)
            pbar.update(chunksize)

def insert_all_files(files_list) :
    dataframe_collection = {}
    for file in files_list :
        # DF wordt gemaakt van elk file in file_list en in de db gezet
        df = add_location(file)
        insert_with_progress(df)


def add_location(file):
    # load CSV file
    org_file = pd.read_csv(file)
    # Maak DF met de benodigde kolommen
    df = org_file[['pnt_id', 'pnt_lat', 'pnt_lon']]
    conditie = [
        # Engelse Werk
        (df['pnt_lat'] >= 52.46) & (df['pnt_lat'] <= 52.54) & (df['pnt_lon'] >= 6.0) & (df['pnt_lon'] <= 6.2),
        # Hammerflier
        (df['pnt_lat'] >= 52.44) & (df['pnt_lat'] <= 52.5) & (df['pnt_lon'] >= 6.5) & (df['pnt_lon'] <= 6.7),
        # Manderveen
        (df['pnt_lat'] >= 52.42) & (df['pnt_lat'] <= 52.48) & (df['pnt_lon'] >= 6.7) & (df['pnt_lon'] <= 6.9),
        # Wierden
        (df['pnt_lat'] >= 52.32) & (df['pnt_lat'] <= 52.41) & (df['pnt_lon'] >= 6.5) & (df['pnt_lon'] <= 6.7),
        # Hasselo
        (df['pnt_lat'] >= 52.28) & (df['pnt_lat'] <= 52.32) & (df['pnt_lon'] >= 6.7) & (df['pnt_lon'] <= 6.9),
        # Weerselo
        (df['pnt_lat'] >= 52.32) & (df['pnt_lat'] <= 52.38) & (df['pnt_lon'] >= 6.8) & (df['pnt_lon'] <= 6.9),
        # Espelose broek
        (df['pnt_lat'] >= 52.28) & (df['pnt_lat'] <= 52.33) & (df['pnt_lon'] >= 6.3) & (df['pnt_lon'] <= 6.4),
        # Sint Jans Klooster
        (df['pnt_lat'] >= 52.63) & (df['pnt_lat'] <= 52.71) & (df['pnt_lon'] >= 5.8) & (df['pnt_lon'] <= 6.2),
        # Rodenmors
        (df['pnt_lat'] >= 52.36) & (df['pnt_lat'] <= 52.42) & (df['pnt_lon'] >= 7.0) & (df['pnt_lon'] <= 7.1),
        # Holten
        (df['pnt_lat'] >= 52.24) & (df['pnt_lat'] <= 52.33) & (df['pnt_lon'] >= 6.4) & (df['pnt_lon'] <= 6.5)]
    #locatie namen
    keuze = ['Engelse Werk', 'Hammerflier', 'Manderveen', 'Wierden', 'Hasselo', 'Weerselo', 'Espelose Broek', 'Holten', 'SintJansKlooster', 'Rodenmors']

    # Maak gebied kolom met juist locatie
    df['locatie'] = np.select(conditie, keuze, default="zoutcavernes")
    return df

#locatie van csv bestanden
path_go = "C:\SkyGeo DATA\\"

#bestandsnamen
files_go = ["prov_overijssel_groningen_rsat2_dsc_xf_v4_ps_hoge_punten.csv",
"prov_overijssel_nl_east_env_dsc_v2_ds_punten.csv"]

files_zo = []
all_files = []

#all_files lijst vullen met juiste csv locaties
for file in files_go :
    all_files.append(path_go + file)

for file in files_zo :
    all_files.append(path_go + file)

#insert alle CSV bestanden in de lijst all_files
insert_all_files(all_files)

