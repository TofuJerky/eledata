#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 15:10:36 2022

@author: igor
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# legenda
popis = pd.read_excel('/home/igor/Desktop/Rocni_zprava_o_trhu_2022_V0.xls',sheet_name ='Popis')

# denni trhy
dt = pd.read_excel('/home/igor/Desktop/Rocni_zprava_o_trhu_2022_V0.xls',sheet_name ='DT ČR')
dtcols = dt.columns

# import a export po hodine
imp_exp = pd.read_excel('/home/igor/Desktop/Rocni_zprava_o_trhu_2022_V0.xls',sheet_name ='DT ČR Import-Export')
iecols = imp_exp.columns

# vnitrodenni trhy
vdt = pd.read_excel('/home/igor/Desktop/Rocni_zprava_o_trhu_2022_V0.xls',sheet_name ='VDT (EUR)')
vdtcols = vdt.columns
















plt.plot(vdt[vdtcols[5]]) # hodinove prumery vdt










































