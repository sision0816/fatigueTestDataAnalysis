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
readFile_original = 'SK200_14_experiment_timeData.csv' # in with csv format and in list
readFile_firstCycle = 'Nr14_cycle1_1kN.csv'
print 'Input the file name you want to write the after filtered time sequence data:'
writeFile_timeData_withTrueStressStrain = 'SK200_14_experiment_timeData_withTrueStresStrain.csv'

#==============================================================================
# #input data file
#==============================================================================

df=pd.read_csv(readFile_original,sep=';')
df_firstCycle = pd.read_csv(readFile_firstCycle, sep=';')

#==============================================================================
# test parameters
#==============================================================================
crossSection = 58.905
gageLength = 15
#==============================================================================
# calculate the Eng. and True stress strain
#==============================================================================
df['Engineering stress MPa'] = df['Kraft kN']*1000/crossSection
df['Engineering strain'] = (df['Dehnung_fullrange_SH46 mm']-df_firstCycle['Dehnung_fullrange_SH46 mm'][0])/(gageLength+df_firstCycle['Dehnung_fullrange_SH46 mm'][0])
df['True stress MPa']= df['Engineering stress MPa']*(1+df['Engineering strain'])
df['True strain'] = np.log(1+df['Engineering strain'])

#==============================================================================
# Write the data to csv file
#==============================================================================
df.to_csv(writeFile_timeData_withTrueStressStrain,sep=';',index=False)

print 'finish'
