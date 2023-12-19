#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created in 2023

@author: massimo
"""

import pandas as pd
import os
import numpy as np


def bw_to_spcsv(dataframe, name):
    """
    Function adapted from previous script to convert csv files into simapro csv format
    'dataframe' [pd.DataFrame] object obtained from importing the csv file table
    'name' [string] name of the output file, e.g. 'myLCI.csv'
    """
    
    output = open(name, 'w')
    # Open destination file and print the standard heading
     
    output.write('{CSV separator: Semicolon}\n')
    output.write('{CSV Format version: 7.0.0}\n')
    output.write('{Decimal separator: .}\n')
    output.write('{Date separator: /}\n')
    output.write('{Short date format: dd/MM/yyyy}\n\n')
     
    # List of fields required
    
    fields = ["Process", "Category type", "Time Period", "Geography",
              "Technology", "Representativeness", "Multiple output allocation",
              "Substitution allocation", "Cut off rules", "Capital goods",
              "Boundary with nature", "Record", "Generator", "Literature references",
              "Collection method", "Data treatment", "Verification",
              "Products", "Materials/fuels", "Resources", "Emissions to air",
              "Emissions to water", "Emissions to soil", "Final waste flows",
              "Non material emission", "Social issues", "Economic issues",
              "Waste to treatment", "End"
             ]
    # Standard value of these fields
    fields_value = ['', '', "Unspecified", "Unspecified", "Unspecified",
                    "Unspecified", "Unspecified", "Unspecified", "Unspecified",
                    "Unspecified", "Unspecified", '', '', '', '', '',
                    "Comment", '', '', '', '', '', '', '', '', '', '', '', ''
                   ]
    
    # Identify the processes
    lci = dataframe.copy()
    lci = lci.replace(0.0, np.nan)
    lci = lci.replace(np.nan, '')
     
    processes = lci[lci["Exchange type"] == "production"]["Activity code"].values

    # Screen through the processes
    for i in range(0, len(processes)):
        
        p_prod = lci[(lci["Activity code"] == processes[i]) & (lci["Exchange type"] == 'production')]
        fields_value[1] = "Material"

        ref_product = (6 * "\"%s\";") % (str(p_prod['Simapro name'].values[0]), str(p_prod['Simapro unit'].values[0]),
                                      str(str(p_prod['Exchange amount'].values[0])), "100%", "not defined", str(p_prod['Activity database'].values[0]))

        fields_value[17] = ref_product
        matfuel_list = []
        raw_list = []
        air_list = []
        water_list = []
        soil_list = []
        finalwaste_list = []
        social_list = []
        economic_list = []
        wastetotreatment_list = []

        # Screen through the inputs and outputs of each process
        
        p_df = lci[(lci["Activity code"] == processes[i]) & (lci["Exchange type"] != 'production')] # p_df stands for "Process dataframe", a dataframe with all exhanges of a process
        
        for ind in p_df.index: # for each indexed row of the dataframe
            
            if p_df['Simapro type'][ind] == '':
                matfuel = (7 * "\"%s\";") % (p_df['Simapro name'][ind], p_df['Simapro unit'][ind], p_df['Exchange amount'][ind], "Undefined", 0, 0, 0)
                matfuel_list.append(matfuel)

            elif p_df['Simapro type'][ind] == 'Raw':
                raw = (8 * "\"%s\";") % (p_df['Simapro name'][ind], '', p_df['Simapro unit'][ind], p_df['Exchange amount'][ind], "Undefined", 0, 0, 0)
                raw_list.append(raw)
                
            elif p_df['Simapro type'][ind] == 'Air':
                air = (8 * "\"%s\";") % (p_df['Simapro name'][ind], '', p_df['Simapro unit'][ind], p_df['Exchange amount'][ind], "Undefined", 0, 0, 0)
                air_list.append(air)
                
            elif p_df['Simapro type'][ind] == 'Water':
                water = (8 * "\"%s\";") % (p_df['Simapro name'][ind], '', p_df['Simapro unit'][ind], p_df['Exchange amount'][ind], "Undefined", 0, 0, 0)
                water_list.append(water)
                    
            elif p_df['Simapro type'][ind] == 'Soil':
                soil = (8 * "\"%s\";") % (p_df['Simapro name'][ind], '', p_df['Simapro unit'][ind], p_df['Exchange amount'][ind], "Undefined", 0, 0, 0)
                soil_list.append(soil)
            
            elif p_df['Simapro type'][ind] == 'Waste':
                waste = (8 * "\"%s\";") % (p_df['Simapro name'][ind], '', p_df['Simapro unit'][ind], p_df['Exchange amount'][ind], "Undefined", 0, 0, 0)
                finalwaste_list.append(waste)
            
            elif p_df['Simapro type'][ind] == 'Social':
                social = (8 * "\"%s\";") % (p_df['Simapro name'][ind], '', p_df['Simapro unit'][ind], p_df['Exchange amount'][ind], "Undefined", 0, 0, 0)
                social_list.append(social)
            
            elif p_df['Simapro type'][ind] == 'Economic':
                economic = (8 * "\"%s\";") % (p_df['Simapro name'][ind], '', p_df['Simapro unit'][ind], p_df['Exchange amount'][ind], "Undefined", 0, 0, 0)
                economic_list.append(economic)
            
            elif p_df['Simapro type'][ind] == 'Wastetotreatment':
                wastetotreatment = (7 * "\"%s\";") % (p_df['Simapro name'][ind], p_df['Simapro unit'][ind], p_df['Exchange amount'][ind], "Undefined", 0, 0, 0)
                wastetotreatment_list.append(wastetotreatment)
                
            # Assign the inputs and outputs to a list
            fields_value[18] = matfuel_list
            fields_value[19] = raw_list
            fields_value[20] = air_list
            fields_value[21] = water_list
            fields_value[22] = soil_list
            fields_value[23] = finalwaste_list
            fields_value[25] = social_list
            fields_value[26] = economic_list
            fields_value[27] = wastetotreatment_list
            
        for f in range (0, len(fields)):  # Important, note the indentation here. f stands for "field"
            
            output.write("%s\n" % fields[f])
            
            if not isinstance(fields_value[f], list):
                
                output.write("%s\n" % fields_value[f])	
            
            else:
                
                for j in fields_value[f]:
                    
                    variable = "%s" % j
                    output.write("%s\n" % variable)
            
            output.write("\n")
    
    output.close()