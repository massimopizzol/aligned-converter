'''
 # @ Author: Ning An
 # @ Create Time: 2025-06-06 14:39:05
 # @ Modified by: Ning An
 # @ Modified time: 2025-06-16 09:26:51
 '''

'''
This script aims to validate the user's input CSV file.
'''

import pandas as pd

def validate_df(df):
    """Field check."""
    # Validate database name
    database = df["Activity database"].unique().tolist()
    if len(database) > 1:
        raise ValueError("Reminder: 'Activity database' column should only include the name of your database. Check if you have more than one database names, otherwise delete all empty rows in your file.")

    # Validate fields in the right order
    act_cols = ['Activity database','Activity code','Activity name','Activity unit','Activity type',
                'Exchange database','Exchange input','Exchange amount','Exchange unit','Exchange type']
    if list(df.columns[:len(act_cols)]) != act_cols:
        raise ValueError("Reminder: The columns in your CSV file must be in the right order, please check the example CSV file.")

    """Validate exchanges are defined."""
    exchange_db = df[df['Exchange database'] == database[0]].copy()
    undefined_inputs = exchange_db[~exchange_db["Exchange input"].isin(df["Activity code"])]
    if len(undefined_inputs["Exchange input"].unique()) > 0:
        raise ValueError(f"Reminder: {undefined_inputs["Exchange input"].tolist()} are undefined in your csv file. \n"
              "Please check:\n"
                 "1. Did you fill the 'Exchange input' cell for each exchange? \n"
                 "2. Did you define the 'Activity code' before you use it as an exchange input? \n"
                 "3. Did you spell it exactly as defined in the 'Activity code' column?")

    """Validate all activities are used."""
    empty_exchanges = df[df["Exchange input"].isna()].copy()
    acts = empty_exchanges["Activity code"].unique()
    unused_acts = [act for act in acts if act not in df["Exchange input"].values]
    if len(unused_acts) > 0:
        raise ValueError(f"Reminder: {unused_acts} is defined but not used in your foreground system.")