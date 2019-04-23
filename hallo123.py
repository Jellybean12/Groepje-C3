import pandas as pd
import numpy as np
import re


def bestand(bestandsnaam):
    nieuwbestand = bestandsnaam.replace("_", " ")
    return nieuwbestand

def get_type(invoer):
        if 'asc' in invoer:
            if 'ds' in invoer:
                if 'hoge' in invoer:
                    return 'HDA'
                else:
                    return 'LDA'
            elif 'hoge' in invoer:
                return 'HPA'
            else:
                return 'LPA'
        elif 'ds' in invoer:
            if 'hoge' in invoer:
                return 'HDD'
            else:
                return 'LDD'
        elif 'hoge' in invoer:
            return 'HPD'
        else:
            return 'LPD'


def get_satalliet(invoer):
    get_type(invoer)
    if 'rsat2' in invoer:
        return 'rsatxf'
    elif 'rsat3' in invoer:
        return 'rsat3'
    else:
        return 'env'

csv = 'prov_overijssel_eindhoven_rsat2_asc_xf_v2_ds_hoge_punten'
hoi = bestand(csv)
#print(get_type(hoi))

def sql(csv):
    type = get_type(csv)
    sat = get_satalliet(csv)
    string = "SELECT sat_id FROM satalliet WHERE sat_naam = "+sat+" AND type ="+type
    resultaat = pd.read_sql(string, engine)
    return resultaat

#bestand('prov_overijssel_eindhoven_env_dsc_v2_ds_punten')
#print(sql(csv,csv))
#doei = get_type(hoi)
#print(doei)
#hallo = get_satalliet(hoi)
#print(hallo)
#txt = txt.replace("_", " ")
#print(txt)



#if 'rsat2' == re.findall("rsat2", txt):
#    print('De satalliet is rsat2')
#else:
#    print('De satalliet is niet rsat2')