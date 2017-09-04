# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 14:09:39 2017

@author: chen_w1
"""

import pandas as pd
import numpy as np
from pandas import DataFrame, read_csv
#==============================================================================
# input the read file name and write file name
#==============================================================================
#print 'Input the file name you want to analysis:' 
readFile_original = 'PSIWATER3.csv' # in with csv format and in list
#print 'Input the file name you want to write the after filtered time sequence data:'
writeFile_timeSequence = 'PSIWATER3TimeData.csv'
#print 'Input the file name you want to write the Max Min data:'
writeFile_maxMin = 'PSIWATER3MaxMinData.csv'
writeFile_maxMin_simple = 'PSIWATER3MaxMinData_simple.csv'

#==============================================================================
# #input data file
#==============================================================================

df=pd.read_csv(readFile_original,sep=';')

#==============================================================================
# #find the starting point of force loading
#==============================================================================
for i in range (len(df.index)):
    if df['Kraft kN'][i:i+2].std() > 0.05:
        break
#delete the before cyclic loading data, filter_df time sequence data
filter_df=df.loc[i:,'Weg mm':'Temperatur grd']
#the Zeit and Zyklus columns
other_df=df[['Zeit s','Zyklus']]
#reset the index of filter_df    
filter_df=filter_df.reset_index(drop=True)
#combine the columns together, output the after filtered dataframe
filtered_df=pd.concat([other_df,filter_df],axis=1)
#==============================================================================
# #delete the after failure data
#==============================================================================
for j in xrange(len(filtered_df.index),0,-1):
    if filtered_df['Kraft kN'][j:j+20].std()>0.01: #or can set larger than 0.1. or can set [j:j+10].std(),just for delete non sense data and save computation time
        break
filtered_df=filtered_df.drop(filtered_df.index[j+1:])
#write the filtered time sequence data into csv
filtered_df.to_csv(writeFile_timeSequence, sep=';', index=False)
#==============================================================================
# #filter the max and min data
#==============================================================================
maxCycle=int(filtered_df['Zyklus'].max())
# itterate each cycle 
dfmax=pd.DataFrame(columns = ['Zyklus','Zeit s','Weg mm','Kraft kN','Sandner_1701_INCEFA mm','Temperatur grd'])
dfmin=pd.DataFrame(columns = ['Zyklus','Zeit s','Weg mm','Kraft kN','Sandner_1701_INCEFA mm','Temperatur grd'])
for cycle in range (1, maxCycle+1):
    print cycle
    df2=filtered_df[filtered_df.Zyklus==cycle]
#may use df2[index=df2.index[df2['Dehnung_fullrange_SH46 mm'].max()]], question: stress max or strain max
    df3=df2.max()
    df4=df2.min()
    dfmax=dfmax.append(df3, ignore_index=True)
    dfmin=dfmin.append(df4, ignore_index=True)
dfmax.columns = ['Zyklus','Zeit Max s','Weg Max mm','Kraft Max kN','Sandner_1701_INCEFA Maxmm','Temperatur Max grd']
dfmin.columns = ['Zyklus','Zeit Min s','Weg Min mm','Kraft Min kN','Sandner_1701_INCEFA Min mm','Temperatur Min grd']
dfMaxMin = pd.merge(dfmax,dfmin,how='outer',on='Zyklus')
dfMaxMin_simple = dfMaxMin[['Zyklus','Kraft Max kN','Kraft Min kN','Sandner_1701_INCEFA Maxmm','Sandner_1701_INCEFA Min mm']]
dfMaxMin_simple.columns = ['Cycles','Force_max kN','Force_min kN', 'Strain_max mm','Strain_min mm']
# write dataframe to csv

dfMaxMin.to_csv(writeFile_maxMin,sep=';',index=False)
dfMaxMin_simple.to_csv(writeFile_maxMin_simple,sep=';',index=False)
  
print 'finish'

