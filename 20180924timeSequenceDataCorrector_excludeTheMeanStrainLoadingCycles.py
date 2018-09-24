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
readFile_original = 'PSIair6.csv' # in with csv format and in list
#print 'Input the file name you want to write the after filtered time sequence data:'
writeFile_timeSequence = 'PSIair6TimeData.csv'

#==============================================================================
# #input data file
#==============================================================================

df=pd.read_csv(readFile_original,sep=';')

#==============================================================================
# #find the starting point of cyclic loading
#==============================================================================

meanStrainLoading_df = df.loc[:430,'Weg mm':'Temperature deg']
cyclicLoading_df=df.loc[430:,'Weg mm':'Temperature deg'] #exclude the mean strain loading cycles
#the Zeit and Zyklus columns
other_df=df[['Zeit s','Zyklus']]
#reset the index of filter_df    
cyclicLoading_df=cyclicLoading_df.reset_index(drop=True)
#combine the columns together, output the after filtered dataframe
cyclicLoading_df=pd.concat([other_df,cyclicLoading_df],axis=1)
#==============================================================================
# #delete the after failure data
#==============================================================================
for j in range(len(cyclicLoading_df.index),1,-1):
    if cyclicLoading_df['Kraft kN'][j:j+20].std()<0.01: #or can set larger than 0.1. or can set [j:j+10].std(),just for delete non sense data and save computation time
        break
cyclicLoading_df=cyclicLoading_df.drop(cyclicLoading_df.index[j+1:])

#==============================================================================
# #delete the non data cycles in the end part
#==============================================================================
for k in range(len(cyclicLoading_df.index)-1,1,-1):
    if np.isnan(cyclicLoading_df['Kraft kN'][k]) == False:
        cyclicLoading_df = cyclicLoading_df.drop(cyclicLoading_df.index[k+2:])
        break
#==============================================================================
# merge the meaStrainLoading and cyclicLoading parts together
#==============================================================================
correctedCycleSequence_df = pd.concat([meanStrainLoading_df,cyclicLoading_df],ignore_index=True)
correctedCycleSequence_df = df[['Zeit s','Zyklus','Weg mm','Kraft kN','epsilon mm','Temperature deg']]
#==============================================================================
# #write the filtered time sequence data into csv
#==============================================================================
correctedCycleSequence_df.to_csv(writeFile_timeSequence, sep=',', index=False)
meanStrainLoading_df.to_csv('meanStrainLoadingCycles.csv',sep=',',index=False)
cyclicLoading_df.to_csv('cyclicLoadingCycles_excludeMeanStrainLoading.csv',sep=',',index=False)


  
print 'finish'

