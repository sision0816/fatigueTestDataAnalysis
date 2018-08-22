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
print 'Input the file name you want to analysis:' 
readFile_original = 'SKA200_08_experiment_timeData_withTrueStresStrain.csv' # in with csv format and in list
print 'Input the file name you want to write the after filtered time sequence data:'
writeFile_maxMinData_withTrueStressStrain = 'SKA200_08_experiment_maxMinData_withTrueStresStrain.csv'

#==============================================================================
# #input data file
#==============================================================================

df=pd.read_csv(readFile_original,sep=';')

#==============================================================================
# #filter the max and min data
#==============================================================================
maxcycle=int(df['Cycle'].max())
# itterate each cycle
dfmax=pd.DataFrame(columns = ['Cycle','Time Sec','Traverse mm','Load kN','Strain mm','Engineering stress MPa','Engineering strain','True stress MPa','True strain'])
dfmin=pd.DataFrame(columns = ['Cycle','Time Sec','Traverse mm','Load kN','Strain mm','Engineering stress MPa','Engineering strain','True stress MPa','True strain'])
for cycle in range (1, maxcycle+1):
    print cycle
    df2=df[df.Cycle==cycle]
  #may use df2[index=df2.index[df2['Dehnung_fullrange_SH46 mm'].max()]], question: stress max or strain max
    df3=df2.max()
    df4=df2.min()
    dfmax=dfmax.append(df3, ignore_index=True)
    dfmin=dfmin.append(df4, ignore_index=True)
dfmax.columns = ['Zyklus','Zeit Max s','Weg Max mm','Kraft Max kN','Dehnung Max mm','Engineering stress Max MPa','Engineering strain Max','True stress Max MPa','True strain Max']
dfmin.columns = ['Zyklus','Zeit Min s','Weg Min mm','Kraft Min kN','Dehnung Min mm','Engineering stress Min MPa','Engineering strain Min','True stress Min MPa','True strain Min']
dfMaxMin = pd.merge(dfmax,dfmin,how='outer',on='Zyklus')
# write dataframe to csv
  
dfMaxMin.to_csv(writeFile_maxMinData_withTrueStressStrain,sep=';',index=False)
    
print 'finish'
