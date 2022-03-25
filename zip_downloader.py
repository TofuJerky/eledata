#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 09:55:39 2022

@author: igor
"""

import wget
import pandas as pd
import numpy as np
import requests, zipfile
from io import BytesIO
from collections import Counter
import ast
#-------------------------------------------------------------

for i in range(10,22):
    url = 'https://www.ote-cr.cz/pubweb/attachments/62_162/20' +str(i) + '/Rocni_zprava_o_trhu_20'+str(i)+'_V0.zip'
    extract_file = '/home/igor/Desktop/dir_data_ote_ele'
    req = requests.get(url)
    zipf= zipfile.ZipFile(BytesIO(req.content))
    zipf.extractall(extract_file)

# beha to, akorat to sem tam hodi error: 'ZipFile' object has no attribute 'ZipFile'

#-------------------------------------------------------------

def get_unzip_save(url,extract_file):
    req = requests.get(url)
    zipf= zipfile.ZipFile(BytesIO(req.content))
    zipf.extractall(extract_file)
#-----------------------------------------------------------------------------MAka to jako svine!

# rocni zpravy - idealne tridit od 2016

#jake sheets jsou v rocnich zpravech - bacha pomale
sheetsin = {i:[] for i in range(10,22)}
for i in range(10,22):
    drt = '/home/igor/Desktop/dir_data_ote_ele/Rocni_zprava_o_trhu_20'+str(i)+'_V0.xls'
    dfsheets = pd.read_excel(drt,None).keys()
    ks = [*dfsheets]
    print(ks)
    sheetsin[i] = ks

allks = []
for i in range(len(sheetsin)):
    allks += [*sheetsin.values()][i]
#---------------------------------------------------------------------------------
pocty = dict(Counter(allks)) # - z tohot vyberu, umazu, conectate, spojim s KZD daty a teplotami, RNN popapa a jedem! 
#---------------------------------------------------------------------------------
np.save('sheet_names_per_rocni_zprava.npy',np.array(sheetsin))
#---------------------------------------------------------------------------------
'''odsud poustet'''

shin = np.load('sheet_names_per_rocni_zprava.npy',allow_pickle=True)
s = ast.literal_eval(str(shin))
allks = []
for i in range(len(s)):
    allks += [*s.values()][i]
pocty = dict(Counter(allks))   
#---------------------------------------------------------------------------------
'''Odchylky'''
def beautify_odchylky(file_dir,sheet): # best for odchylky
    tdf = pd.read_excel(file_dir,sheet_name = sheet)
    for i in range(len(tdf.columns)):
        #print(tdf.columns)
        tdf.rename(columns={'Unnamed: '+str(i):tdf.loc[4][i]  }, inplace=True)
    tdf.drop([0, 1,2,3,4], inplace = True)
    tdf = tdf.reset_index(drop = True)        
    return tdf

''' RE + / RE-'''
def beautify_RE(file_dir,sheet):
    tdf0 = pd.read_excel(file_dir,sheet_name = sheet)
    cols = tdf0.columns
    new = tdf0[[cols[i] for i in range(4)]].copy()
    for i in range(4):
        new.rename(columns={'Unnamed: '+str(i):new.loc[4][i]  }, inplace=True)
    new.drop([0, 1,2,3,4], inplace = True)
    new = new.reset_index(drop = True)  
    return new
#---------------------------------------------------------------------------------

''' chci to obecne'''

def pretty_df(file,sheet,wanted_cols):
    # file = directory
    # sheet = sheet_name
    # wanted_cols = [0,1,2..]
    df0 = pd.read_excel(file,sheet_name = sheet)
    cols = df0.columns
    new = df0[[cols[i] for i in wanted_cols]].copy() # just ones i want
    for i in range(len(new.columns)):
        new.rename(columns={'Unnamed: '+str(i):new.loc[4][i]  }, inplace=True)       
    new.drop([0, 1,2,3,4], inplace = True)
    new = new.reset_index(drop = True)  
    return new

od = pretty_df('/home/igor/Desktop/dir_data_ote_ele/Rocni_zprava_o_trhu_2021_V0.xls','Odchylky',[0,1,2,3,4,5,6,7,8,9,10]) #odchylky
rem = pretty_df('/home/igor/Desktop/dir_data_ote_ele/Rocni_zprava_o_trhu_2021_V0.xls','RE -',[0,1,2,3]) #re-
rep = pretty_df('/home/igor/Desktop/dir_data_ote_ele/Rocni_zprava_o_trhu_2021_V0.xls','RE +',[0,1,2,3]) #re+
erd = pretty_df('/home/igor/Desktop/dir_data_ote_ele/Rocni_zprava_o_trhu_2021_V0.xls','ERD',[0,1,2]) # bilat. vnitrostatni kontrakty
imp = pretty_df('/home/igor/Desktop/dir_data_ote_ele/Rocni_zprava_o_trhu_2021_V0.xls','Import',[0,1,2]) #import
exp = pretty_df('/home/igor/Desktop/dir_data_ote_ele/Rocni_zprava_o_trhu_2021_V0.xls','Export',[0,1,2]) # export
DT = pretty_df('/home/igor/Desktop/dir_data_ote_ele/Rocni_zprava_o_trhu_2021_V0.xls','DT ČR',[0,1,2,3,4,5,6,7,8,9,10,11]) # DT cr




rep = beautify_RE('/home/igor/Desktop/dir_data_ote_ele/Rocni_zprava_o_trhu_2021_V0.xls','RE +')
od = beautify_odchylky('/home/igor/Desktop/dir_data_ote_ele/Rocni_zprava_o_trhu_2021_V0.xls','Odchylky')


tdf = pd.read_excel('/home/igor/Desktop/dir_data_ote_ele/Rocni_zprava_o_trhu_2021_V0.xls',sheet_name = 'RE +')

for i in range(len(tdf.columns)):
    tdf.rename(columns={'Unnamed: '+str(i):tdf.loc[4][i]  }, inplace=True)
tdf = tdf.reset_index(drop = True)
cols = tdf.columns
tdf.drop([0, 1,2,3,4], inplace = True)

df = tdf.head()






