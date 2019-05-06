import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm

def chunker(seq, size):
    # from http://stackoverflow.com/a/434328
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def insert_with_progress(df):
    #maak connectie met database
    con = create_engine('postgresql://postgres:Welkom01!@10.30.1.10:5432/POC')
    # set chunksize
    chunksize = int(len(df) / 10)
    with tqdm(total=len(df)) as pbar:
        for i, cdf in enumerate(chunker(df, chunksize)):
            # chunked df toevoegen aan database in tabel boor_locatie
            cdf.to_sql('boor_locatie', con=con, if_exists='append', index=False)
            pbar.update(chunksize)

# is nu leeg, want je moet niet zomaar weer in de database kunnen doen
df_inactief = pd.read_csv("")

insert_with_progress(df_inactief)
