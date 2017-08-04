# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 18:48:41 2016

@author: chen_w1
"""

import pandas as pd
import numpy as np
from pandas import DataFrame, read_csv,read_excel
import scipy
import scipy.stats
#==============================================================================
# input the read file name and write file name
#==============================================================================
#print 'Input the file name you want to analysis:' 
readFile_timeSequence = 'experimentTimeData.csv' # in with csv format and in list
#print 'Input the file name of first cycle:' 
readFile_firstCycle =  'Nr19_cycle1_1kN.csv'
#print 'Input the file name you want to write the after mechanical analysis data:'
writeFile_mechanicalAnalysisData = 'experimentHysteresisMechanicalAanalysis.csv'

#==============================================================================
# read the csv data file into dataframe
#==============================================================================

df=pd.read_csv(readFile_timeSequence,sep=';')

#==============================================================================
# specimen and test parameters
#==============================================================================

firstCycleFile = pd.read_csv(readFile_firstCycle,sep=';')
extensormeterInitialValue = firstCycleFile['Dehnung_fullrange_SH46 mm'][0]
crossSection = 58.905
gageLength = 15
yieldStrain = 0.0005

#==============================================================================
# # Stress strain calculation and transfer to stress strain data
#==============================================================================

df['Stress MPa']=pow(10,3)*df['Kraft kN']/crossSection #Stress unite in MPa
df['Strain']=(df['Dehnung_fullrange_SH46 mm']-extensormeterInitialValue)/(gageLength+extensormeterInitialValue)

#==============================================================================
# itterate each cycle
#==============================================================================

# determine the largest cycle number
maxCycle=int(df['Zyklus'].max())
# define the output dataframe of max min data
dfOutput = pd.DataFrame(columns = ['Cycle','Stress Max MPa','Stress Min MPa','Stress Amplitude MPa','Stress Mean MPa','Strain Max','Strain Min','Strain Amplitude','Strain Mean', 'Elastic Modulus GPa', 'Yield Stress MPa','Elastic Strain','Plastic Strain', 'Effective Stress MPa','Back Stress MPa'])

for cycle in range (1, maxCycle+1):
   loop=df[df.Zyklus==cycle]
   strainMax = loop['Strain'].max()
   strainMin = loop['Strain'].min()
   strainAmp = (strainMax - strainMin)/2
   strainMean = (strainMax + strainMin)/2
   stressMax = loop['Stress MPa'].max()
   stressMin = loop['Stress MPa'].min()
   stressAmp = (stressMax - stressMin)/2
   stressMean = (stressMax + stressMin)/2
#  return the index of data of max strain
   maxStrainCount = loop.Strain[loop.Strain==strainMax].index.tolist()[0]
# regression the linear part, calculate elastic modulus
   if loop.index.max()< maxStrainCount+50: #if the last cycle is not long enough will cause error report in the regression, if the loop length not enough, break
       break
   xx = loop.loc[maxStrainCount+10:maxStrainCount+50, :]['Strain'] #try to get a series not df or will get error report 'NotImplementedError: Only 2-level MultiIndex are supported.'
   yy = loop.loc[maxStrainCount+10:maxStrainCount+50, :]['Stress MPa']
   slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(xx,yy)
   eModulus = 0.001*slope
   intercept = intercept
# count the acquisition point per cycle
   counts=len(loop.index)
# itterate each data point, yield stress, effective stress and back stress 
   for count in range(maxStrainCount+50,maxStrainCount+counts):  
       if loop['Strain'][count]/((loop['Stress MPa'][count]-intercept)/eModulus)<(1-yieldStrain):
          yieldStress = loop['Stress MPa'][count]
#          print 'yield point find'
          break
       if loop['Stress MPa'][count] < stressMean:
           yieldStress = eModulus*yieldStrain
           print 'yield point not find'
           break
   effectiveStress = stressMax - yieldStress
   backStress = yieldStress - stressMin
   elasticStrain = 0.001*stressAmp/eModulus
   plasticStrain = strainAmp - elasticStrain
   dfOutput.loc[len(dfOutput)] = [cycle,stressMax,stressMin,stressAmp,stressMean,strainMax,strainMin,strainAmp,strainMean,eModulus,yieldStress,elasticStrain,plasticStrain,effectiveStress,backStress]

#==============================================================================
#  write dataframe to  csv
#==============================================================================
dfOutput.to_csv(writeFile_mechanicalAnalysisData, sep=';', index = False)

print 'finish'   



