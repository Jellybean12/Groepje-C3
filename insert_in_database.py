import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm

def chunker(seq, size):
    """Deelt een dataframe op aan de hand van de dataframe lengte gedeeld door de meegegeven size."""
    # from http://stackoverflow.com/a/434328
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def insert_with_progress(df, tablename):
    """Importeert een dataframe in de aangegeven tabel."""
    #maak connectie met database
    con = create_engine('postgresql://postgres:Welkom01!@10.30.1.10:5432/POC')
    # set chunksize
    chunksize = int(len(df) / 10)
    with tqdm(total=len(df)) as pbar:
        for i, cdf in enumerate(chunker(df, chunksize)):
            # chunked df toevoegen aan database in tabel boor_locatie
            cdf.to_sql(tablename, con=con, if_exists='append', index=False)
            pbar.update(chunksize)

def create_dataframe(filename) :
    """Maakt een dataframe van een meegegeven csv filename."""
    df = pd.read_csv(filename)
    return df
