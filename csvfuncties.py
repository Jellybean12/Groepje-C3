import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import re

def bestand(bestandsnaam):
    #Deze funtie verwijderd de lage streepjes uit een bestandsnaam
    nieuwbestand = bestandsnaam.replace("_", " ")
    return nieuwbestand

csv = 'prov_overijssel_nl_east_env_dsc_v2_ps_punten'
hoi = bestand(csv)

def get_type(invoer):
    """Deze functie bepaalt het type(HPA,HPD etc) op basis van de invoer"""
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

print(get_type(hoi))

