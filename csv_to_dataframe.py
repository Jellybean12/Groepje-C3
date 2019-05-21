import numpy as np
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:Welkom01!@10.30.1.10:5432/POC')

path_go = "go\\"
path_zc = "zc\\"

files_go = ["prov_overijssel_eindhoven_rsat2_asc_xf_v2_ds_hoge_punten.csv",
"prov_overijssel_eindhoven_rsat2_asc_xf_v2_ds_lage_punten.csv",
"prov_overijssel_eindhoven_rsat2_asc_xf_v2_ps_hoge_punten.csv",
"prov_overijssel_eindhoven_rsat2_asc_xf_v2_ps_lage_punten.csv",
"prov_overijssel_groningen_rsat2_asc_xf_v2_ds_hoge_punten.csv",
"prov_overijssel_groningen_rsat2_asc_xf_v2_ds_lage_punten.csv",
"prov_overijssel_groningen_rsat2_asc_xf_v2_ps_hoge_punten.csv",
"prov_overijssel_groningen_rsat2_asc_xf_v2_ps_lage_punten.csv",
"prov_overijssel_groningen_rsat2_dsc_xf_v4_ds_hoge_punten.csv",
"prov_overijssel_groningen_rsat2_dsc_xf_v4_ds_lage_punten.csv",
"prov_overijssel_groningen_rsat2_dsc_xf_v4_ps_hoge_punten.csv",
"prov_overijssel_groningen_rsat2_dsc_xf_v4_ps_lage_punten.csv",
"prov_overijssel_nl_east_env_dsc_v2_ds_punten.csv",
"prov_overijssel_nl_east_env_dsc_v2_ps_punten.csv",
"prov_overijssel_nl_east_rsat2_dsc_s3_v3_ds_punten.csv",
"prov_overijssel_nl_east_rsat2_dsc_s3_v3_ps_punten.csv",
"prov_overijssel_twente_rsat2_dsc_xf_v4_ds_hoge_punten.csv",
"prov_overijssel_twente_rsat2_dsc_xf_v4_ds_lage_punten.csv",
"prov_overijssel_twente_rsat2_dsc_xf_v4_ps_hoge_punten.csv",
"prov_overijssel_twente_rsat2_dsc_xf_v4_ps_lage_punten.csv"]

files_zc = ["prov_overijssel_eindhoven_rsat2_asc_xf_v2_ds_hoge_punten.csv",
"prov_overijssel_eindhoven_rsat2_asc_xf_v2_ds_lage_punten.csv",
"prov_overijssel_eindhoven_rsat2_asc_xf_v2_ps_hoge_punten.csv",
"prov_overijssel_eindhoven_rsat2_asc_xf_v2_ps_lage_punten.csv",
"prov_overijssel_nl_east_env_dsc_v2_ds_punten.csv",
"prov_overijssel_nl_east_env_dsc_v2_ps_punten.csv",
"prov_overijssel_nl_east_rsat2_dsc_s3_v3_ds_punten.csv",
"prov_overijssel_nl_east_rsat2_dsc_s3_v3_ps_punten.csv",
"prov_overijssel_twente_rsat2_dsc_xf_v4_ds_hoge_punten.csv",
"prov_overijssel_twente_rsat2_dsc_xf_v4_ds_lage_punten.csv",
"prov_overijssel_twente_rsat2_dsc_xf_v4_ps_hoge_punten.csv",
"prov_overijssel_twente_rsat2_dsc_xf_v4_ps_lage_punten.csv"]

all_filenames = []

for file in files_go :
    all_filenames.append(path_go + file)
for file in files_zc :
    all_filenames.append(path_zc + file)

def remove_underscores(filename):
    """Deze funtie verwijderd de lage streepjes uit een bestandsnaam"""
    new_filename = filename.replace("_", " ")
    return new_filename

def get_type(input):
    """Deze functie bepaalt het type(HPA,HPD etc) op basis van de invoer"""
    invoer = remove_underscores(input)
    #Als ascending, ds en hoge in invoer zit, return HDA
    if (' env ' in invoer or ' v3 ' in invoer):
        if ' ds ' in invoer:
            return 'DD'
        elif ' ps ' in invoer:
            return 'PD'
        else :
            raise ValueError('Geen goede bestandsnaam!')
    elif ' asc ' in invoer:
        if ' ds ' in invoer:
            if ' hoge ' in invoer:
                return 'HDA'
            #Als dit niet zo is, return LDA
            elif ' lage ' in invoer:
                return 'LDA'
            else :
                raise ValueError('Geen goede bestandsnaam!')
        #Als er hoge, ps en asc inzit, return HPA
        elif ' hoge ' in invoer:
            return 'HPA'
        elif ' lage ' in invoer:
            return 'LPA'
        else :
            raise ValueError('Geen goede bestandsnaam!')
    #Als er ds, hoge en andere lage inzit, return HDD of LDD
    elif ' ds ' in invoer:
        if ' hoge ' in invoer:
            return 'HDD'
        elif ' lage ' in invoer:
            return 'LDD'
        else :
            raise ValueError('Geen goede bestandsnaam!')
    #Als er hoge inzit, return HPD
    elif ' hoge ' in invoer:
        return 'HPD'
    #anders, return LPD
    elif ' lage ' in invoer:
        return 'LPD'
    else:
        raise ValueError('Geen goede bestandsnaam!')

def get_satelliet(input):
    invoer = remove_underscores(input)
    #Als env in de naam zit, return env
    if ' env ' in invoer:
        return 'env'
    #Als s3 in de naam zit, return rsats3
    elif ' s3 ' in invoer:
        return 'rsats3'
    #Anders is het automatisch rsatxf
    else:
        return 'rsatxf'

def convert_dataframe_datums(file) :
    # 1. Begin met een gewone dataframe van de csv
    original_df = pd.read_csv(file)
    # 2. Replace de d_ in de datum kolommen
    original_df.columns = original_df.columns.str.replace('d_', '')
    # 3. Maak een temp dataframe met alleen de datum kolommen
    temp = original_df.iloc[:,9:-2]
    # 4. Verander de namen van de datum kolommen naar date
    temp.columns = pd.to_datetime(temp.columns).date
    # 5. Voeg de 'pnt_id' kolom van de oorspronkelijke csv toe aan de temp
    temp['pnt_id'] = original_df['pnt_id']
    # 6. Maak van de temp een dataframe waarbij de datum kolommen values worden
    temp = temp.set_index('pnt_id').stack().reset_index()
    # 7. Verander de kolom namen van de temp dataframe
    result = temp.rename(columns={'level_1':'datum', 0:'meting'})
    # 8. Selecteer het id van de betreffende satelliet
    satname = get_satelliet(file)
    sattype = get_type(file)
    query = "SELECT sat_id FROM satelliet WHERE sat_naam = '" + satname + "' AND type ='" + sattype +"'"
    sat_id = pd.read_sql_query(query, engine).iloc[0, 0]
    # 9. Maak een nieuwe kolom 'sat_id' met het betreffende id en voeg die toe aan de dataframe
    result['sat_id'] = sat_id
    return result

