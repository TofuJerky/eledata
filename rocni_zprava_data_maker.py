#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 12:27:30 2022

@author: igor
"""

import pandas as pd
import numpy as np
from collections import Counter
from functools import reduce

def pretty_df(file,sheet,wanted_cols,sufix):
    # file = directory
    # sheet = sheet_name
    # wanted_cols = [0,1,2..]
    # sufix = str 
    df0 = pd.read_excel(file,sheet_name = sheet)
    cols = df0.columns
    new = df0[[cols[i] for i in wanted_cols]].copy() # just ones i want
    for i in range(len(new.columns)):
        if (new.loc[4][i] == 'Den') or (new.loc[4][i] == 'Hodina'):
            new.rename(columns={'Unnamed: '+str(i):new.loc[4][i]  }, inplace=True)     
        else:
            new.rename(columns={'Unnamed: '+str(i):new.loc[4][i]+''+sufix }, inplace=True) 
    new.drop([0, 1,2,3,4], inplace = True)
    new = new.reset_index(drop = True)  
    return new

def advanced_pretty_df(file,sheet,wanted_cols,names1,names2,sufix): #jede!
    # file = directory
    # sheet = sheet_name
    # wanted_cols = [0,1,2..]
    # names1/2 = index where are col names - lets merge them
    # sufix = str
    df0 = pd.read_excel(file,sheet_name = sheet)
    cols = df0.columns
    new = df0[[cols[i] for i in wanted_cols]].copy() # just ones i want
    
    # n12 merge:
    n1 = new.loc[names1]
    n2 = new.loc[names2]
       
    n1.fillna(0,inplace = True)
    n2.fillna(0,inplace = True)
    for i in range(len(n1)):
        l = list(n1)
        if l[i] == 0:
            n1[i] = n1[i-1]
        if n2[i] !=0:
            n2[i] = n1[i] + '/' +str(n2[i])
        else:
            n2[i] = n1[i]
       
    new.loc[names1] = n1
    new.loc[names2] = n2
    
    for i in range(len(new.columns)):
        if (new.loc[names2][i] == 'Den') or (new.loc[names2][i] == 'Hodina'):
            new.rename(columns={'Unnamed: '+str(i):new.loc[names2][i]  }, inplace=True)       
        else:
            new.rename(columns={'Unnamed: '+str(i):new.loc[names2][i] + ''+sufix }, inplace=True)  
    new.drop([k for k in range(names2+1)], inplace = True)
    new = new.reset_index(drop = True)  
    return new



od = pretty_df('/home/igor/Desktop/dir_data_ote_ele/Rocni_zprava_o_trhu_2021_V0.xls','Odchylky',[0,1,2,3,4,5,6,7,8,9,10],'od') #odchylky
rem = pretty_df('/home/igor/Desktop/dir_data_ote_ele/Rocni_zprava_o_trhu_2021_V0.xls','RE -',[0,1,2,3],'rem') #re-
rep = pretty_df('/home/igor/Desktop/dir_data_ote_ele/Rocni_zprava_o_trhu_2021_V0.xls','RE +',[0,1,2,3],'rep') #re+
erd = pretty_df('/home/igor/Desktop/dir_data_ote_ele/Rocni_zprava_o_trhu_2021_V0.xls','ERD',[0,1,2],'erd') # bilat. vnitrostatni kontrakty
imp = pretty_df('/home/igor/Desktop/dir_data_ote_ele/Rocni_zprava_o_trhu_2021_V0.xls','Import',[0,1,2],'imp') #import
exp = pretty_df('/home/igor/Desktop/dir_data_ote_ele/Rocni_zprava_o_trhu_2021_V0.xls','Export',[0,1,2],'exp') # export
dt = pretty_df('/home/igor/Desktop/dir_data_ote_ele/Rocni_zprava_o_trhu_2021_V0.xls','DT ČR',[0,1,2,3,4,5,6,7,8,9,10,11],'DT') # DT cr

# Indexy DT - nema hodinova data, tj nepouziju - prozatim
# DTie = pd.read_excel('/home/igor/Desktop/dir_data_ote_ele/Rocni_zprava_o_trhu_2021_V0.xls',sheet_name = 'DT ČR Import-Export')
# DT CR imp-Exp : data maji jen pul roku for_whatever_fukin_reason, snad nebude treba - navic dost slozita struktura


mc = advanced_pretty_df('/home/igor/Desktop/dir_data_ote_ele/Rocni_zprava_o_trhu_2021_V0.xls',
                        sheet = 'Market Coupling 4MMC',
                        wanted_cols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],
                        names1 =3,
                        names2 = 4,
                        sufix = 'MC') # bacha jen pul roku! Market Coupling

vdt = pretty_df('/home/igor/Desktop/dir_data_ote_ele/Rocni_zprava_o_trhu_2021_V0.xls','VDT (EUR)',[0,1,2,3,4,5,6,7,8,9,10,11],'VDT') # DT cr



dfs = [od,rem,rep,erd,imp,exp,dt,vdt]

tot = pd.concat(dfs, join='outer', axis=1)

tot = tot.loc[:,~tot.columns.duplicated()] # odstrani duplikatni cols

tot.to_csv('/home/igor/Desktop/rocni_zprava_21_tot.csv',index=False)













