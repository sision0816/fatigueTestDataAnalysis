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
readFile_original = 'SKA200_08_experiment_timeData.csv' # in with csv format and in list
readFile_firstCycle = 'SKA200_08_cycle1_1kN.csv'
print 'Input the file name you want to write the after filtered time sequence data:'
writeFile_timeData_withTrueStressStrain = 'SKA200_08_experiment_timeData_withTrueStresStrain.csv'

#==============================================================================
# #input data file
#==============================================================================

df=pd.read_csv(readFile_original,sep=';')
df_firstCycle = pd.read_csv(readFile_firstCycle, sep=',')
#==============================================================================
# test parameters
#==============================================================================
crossSection = 58.905
gageLength = 15
#==============================================================================
# calculate the Eng. and True stress strain
#==============================================================================
df['Engineering stress MPa'] = df['Load kN']*1000/crossSection
df['Engineering strain'] = (df['Strain mm']-df_firstCycle['Strain mm'][0])/(gageLength+df_firstCycle['Strain mm'][0])
df['True stress MPa']= df['Engineering stress MPa']*(1+df['Engineering strain'])
df['True strain'] = np.log(1+df['Engineering strain'])

print 'finish'
