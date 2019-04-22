import pandas as pd
import numpy as np
import re


def bestand(bestandsnaam):
    bestandsnaam = bestandsnaam.replace("_", " ")
    print(bestandsnaam)
    if 'rsat2' in bestandsnaam:
        print("rsat2")
    elif 'env' in bestandsnaam:
        print('env')
    elif 'rsat3' in bestandsnaam:
        print('rsat3')

bestand('prov_overijssel_eindhoven_rsat3')
#txt = 'prov_overijssel_eindhoven_rsat2_asc_xf_v2_ds_hoge_punten'

#txt = txt.replace("_", " ")
#print(txt)



#if 'rsat2' == re.findall("rsat2", txt):
#    print('De satalliet is rsat2')
#else:
#    print('De satalliet is niet rsat2')