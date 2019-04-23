import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import re

def bestand(bestandsnaam):
    #Deze funtie verwijderd de lage streepjes uit een bestandsnaam
    nieuwbestand = bestandsnaam.replace("_", " ")
    return nieuwbestand

csv = 'prov_overijssel_eindhoven_rsat2_asc_xf_v2_ds_hoge_punten'
hoi = bestand(csv)

def get_type(invoer):
    #Deze functie bepaalt het type(HPA,HPD etc) op basis van de invoer
        #Als ascending, ds en hoge in invoer zit, return HDA
        if 'asc' in invoer:
            if 'ds' in invoer:
                if 'hoge' in invoer:
                    return 'HDA'
                #Als dit niet zo is, return LDA
                else:
                    return 'LDA'
            #Als er hoge, ps en asc inzit, return HPA
            elif 'hoge' in invoer:
                return 'HPA'
            else:
                return 'LPA'
        #Als er ds, hoge en andere lage inzit, return HDD of LDD
        elif 'ds' in invoer:
            if 'hoge' in invoer:
                return 'HDD'
            else:
                return 'LDD'
        #Als er hoge inzit, return HPD
        elif 'hoge' in invoer:
            return 'HPD'
        #anders, return LPD
        else:
            return 'LPD'


def get_satalliet(invoer):
    #Als rsat2 in de naam zit, return rsatxf
    if 'rsat2' in invoer:
        return 'rsatxf'
    #Als rsat3 in de naam zit, return rsat3
    elif 'rsat3' in invoer:
        return 'rsat3'
    #Anders is het automatisch env
    else:
        return 'env'


def sql(csv):
    #Deze functie haalt de gegevens uit de SQL database
    #Engine aanmaken
    engine = create_engine('postgresql://postgres:Welkom01!@10.30.1.10:5432/POC')
    #Type functie aanroepen om het type te bepalen
    type = get_type(csv)
    #Sat functie om de satelliet te bepalen
    sat = get_satalliet(csv)
    #SQL string
    string = "SELECT sat_id FROM satelliet WHERE sat_naam = '" + sat + "' AND type ='" + type+"'"
    #SQL opzetten en uitvoeren
    resultaat = pd.read_sql(string, engine)
    print(resultaat)

print(sql(hoi))

