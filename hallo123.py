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
    if 'rsat2' in invoer:
        return 'rsatxf'
    elif 'rsat3' in invoer:
        return 'rsat3'
    else:
        return 'env'

#bestand('prov_overijssel_eindhoven_env_dsc_v2_ds_punten')
csv = 'prov_overijssel_eindhoven_rsat2_asc_xf_v2_ds_hoge_punten'
hoi = bestand(csv)
doei = get_type(hoi)
print(doei)
hallo = get_satalliet(hoi)
print(hallo)
#txt = txt.replace("_", " ")
#print(txt)



#if 'rsat2' == re.findall("rsat2", txt):
#    print('De satalliet is rsat2')
#else:
#    print('De satalliet is niet rsat2')