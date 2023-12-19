#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 15:21:32 2017

@author: massimo
"""


import pandas as pd
import numpy as np

def lci_to_bw2(df):
    '''A function to convert a pandas Dataframe to a dictionary
    to be converted in a database in bw2'''
    
    act_cols = ['Activity database','Activity code','Activity name','Activity unit','Activity type',
                'Exchange database','Exchange input','Exchange amount','Exchange unit','Exchange type'] # fields that need to be in the right order
    other_cols = [col for col in df.columns if col not in act_cols]
    mydb = df[act_cols + other_cols] # reordered dataframe

    if 'Exchange uncertainty type' in mydb.columns:
        mydb['Exchange uncertainty type'] = mydb['Exchange uncertainty type'].fillna(0).astype(int) # uncertainty type as integers

    act_keys_raw = list(mydb.columns[0:5]) # info for activities
    act_keys_bw2 = [i.replace('Activity ','') for i in act_keys_raw]
    
    exc_keys_raw = list(mydb.columns[5:]) # info for exchanges
    exc_keys_bw2 = [i.replace('Exchange ','') for i in exc_keys_raw]
    
    def exc_to_dict(df_data, some_list):
        exc_data = (pd.DataFrame(list(df_data.values), index = list(exc_keys_bw2))).T
        exc_data = exc_data.dropna(axis=1, how='any') # remove columns without data
        e_values = (exc_data.values).tolist()[0]
        e_values = [(e_values[0],e_values[1])] + e_values[2:]
        some_list.append(dict(zip(list(exc_data.columns)[1:], e_values)))
        
    def act_to_dict(act_data):
        a_keys = act_keys_bw2[2:] + ['exchanges']
        return dict(zip(a_keys, act_data))
    
    def bio_to_dict(bio_data):
        b_keys = act_keys_bw2[2:]
        return dict(zip(b_keys, bio_data))
        
    
    db_keys = []
    db_values =[]
    
    
    for act in mydb['Activity code'].unique():
    
        sel = mydb[mydb['Activity code'] == act] # select each unique ID (each of them is an activity)
        db_key = (list(sel['Activity database'])[0], list(sel['Activity code'])[0])
        db_keys.append(db_key)
        
        if list(sel['Activity type'].unique())[0] == 'biosphere':
                    
            my_bio_data = list(sel.iloc[0,2:5].values)
            db_value = bio_to_dict(my_bio_data)
            db_values.append(db_value)
        
        else:
            my_exc = []
            for i in range(sel.shape[0]):
                exc_to_dict(sel.iloc[i,5:],my_exc)
            
            my_act_data = list(sel.iloc[0,2:5].values) + [my_exc]
            db_value = act_to_dict(my_act_data)
            db_values.append(db_value)
        
     
    bw2_db = dict(zip(db_keys, db_values))
    
    return bw2_db # We have a dictionary ready to be converted into bw database.