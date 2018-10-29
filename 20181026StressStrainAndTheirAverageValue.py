# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 15:20:01 2018

@author: chen_w1
"""

import pandas as pd
import numpy as np
from pandas import DataFrame, read_csv
#==============================================================================
# input the read file name and write file name
#==============================================================================
#print 'Input the file name you want to write the after filtered time sequence data:'
readFile_maxMinData = 'SKA200_27_experiment_maxMinData_binded.csv'
readFile_firstCycle = 'SKA200_27_cycle1_0.8533kN.CSV'
#print 'Input the file name you want to write the Max Min data:'
writeFile_maxMinDataWithStressStrainAndTheirAverageValue = 'SKA200_27_experiment_maxMinData_binded_withStressStrainAndTheirAverageValue.csv'

#==============================================================================
# #input data file
#==============================================================================
maxMinData_df=pd.read_csv(readFile_maxMinData,sep=';')
firstCycle_df=pd.read_csv(readFile_firstCycle,sep=',')

#==============================================================================
# Test parameter and specimen geometry
#==============================================================================
initialExtensoMeterValue = firstCycle_df['Strain mm'][0]
extensometerGageLength = 15
specimenWallCrossSection = 50.2655
#==============================================================================
# calculate the corresponding stress & strain
#==============================================================================
maxMinStressStrainData_df = pd.DataFrame(columns = ['Cycle','Stress Max MPa','Stress Min MPa','Stress amplitude MPa','Mean stress MPa','Strain Max','Strain Min','Strain amplitude','Mean strain','Average stress Max MPa','Average stress Min MPa','Average stress amplitude MPa','Average mean stress MPa','Average strain Max','Average strain Min','Average strain amplitude','Average mean strain'])
maxMinStressStrainData_df['Cycle'] =  maxMinData_df['Zyklus']
maxMinStressStrainData_df['Stress Max MPa'] = maxMinData_df['Kraft Max kN']*1000/specimenWallCrossSection
maxMinStressStrainData_df['Stress Min MPa'] = maxMinData_df['Kraft Min kN']*1000/specimenWallCrossSection
maxMinStressStrainData_df['Strain Max'] = (maxMinData_df['Dehnung Max mm'] - initialExtensoMeterValue)/(15+initialExtensoMeterValue)
maxMinStressStrainData_df['Strain Min'] = (maxMinData_df['Dehnung Min mm'] - initialExtensoMeterValue)/(15+initialExtensoMeterValue)
maxMinStressStrainData_df['Stress amplitude MPa'] = (maxMinStressStrainData_df['Stress Max MPa'] - maxMinStressStrainData_df['Stress Min MPa'])/2
maxMinStressStrainData_df['Mean stress MPa'] = (maxMinStressStrainData_df['Stress Max MPa'] + maxMinStressStrainData_df['Stress Min MPa'])/2
maxMinStressStrainData_df['Strain amplitude'] = (maxMinStressStrainData_df['Strain Max'] - maxMinStressStrainData_df['Strain Min'])/2
maxMinStressStrainData_df['Mean strain'] = (maxMinStressStrainData_df['Strain Max'] + maxMinStressStrainData_df['Strain Min'])/2

sum_stressMax = 0
sum_stressMin = 0
sum_stressAmplitude = 0
sum_meanStress = 0
sum_strainMax = 0
sum_strainMin = 0
sum_strainAmplitude = 0
sum_meanStrain = 0

maxIndex = maxMinData_df.idxmax()[0]
for i in range (maxIndex):
    sum_stressMax += maxMinStressStrainData_df['Stress Max MPa'][i]*(maxMinStressStrainData_df['Cycle'][i+1]-maxMinStressStrainData_df['Cycle'][i])
    sum_stressMin += maxMinStressStrainData_df['Stress Min MPa'][i]*(maxMinStressStrainData_df['Cycle'][i+1]-maxMinStressStrainData_df['Cycle'][i])
    sum_stressAmplitude += maxMinStressStrainData_df['Stress amplitude MPa'][i]*(maxMinStressStrainData_df['Cycle'][i+1]-maxMinStressStrainData_df['Cycle'][i])
    sum_meanStress += maxMinStressStrainData_df['Mean stress MPa'][i]*(maxMinStressStrainData_df['Cycle'][i+1]-maxMinStressStrainData_df['Cycle'][i])
    sum_strainMax += maxMinStressStrainData_df['Strain Max'][i]*(maxMinStressStrainData_df['Cycle'][i+1]-maxMinStressStrainData_df['Cycle'][i])
    sum_strainMin += maxMinStressStrainData_df['Strain Min'][i]*(maxMinStressStrainData_df['Cycle'][i+1]-maxMinStressStrainData_df['Cycle'][i])
    sum_strainAmplitude += maxMinStressStrainData_df['Strain amplitude'][i]*(maxMinStressStrainData_df['Cycle'][i+1]-maxMinStressStrainData_df['Cycle'][i])
    sum_meanStrain += maxMinStressStrainData_df['Mean strain'][i]*(maxMinStressStrainData_df['Cycle'][i+1]-maxMinStressStrainData_df['Cycle'][i])

#==============================================================================
# calculate the average value
#==============================================================================
maxCycle = maxMinData_df['Zyklus'].max() 

maxMinStressStrainData_df['Average stress Max MPa'][0] = sum_stressMax/maxCycle
maxMinStressStrainData_df['Average stress Min MPa'][0] = sum_stressMin/maxCycle
maxMinStressStrainData_df['Average stress amplitude MPa'][0] = sum_stressAmplitude/maxCycle
maxMinStressStrainData_df['Average mean stress MPa'][0] = sum_meanStress/maxCycle
maxMinStressStrainData_df['Average strain Max'][0] = sum_strainMax/maxCycle
maxMinStressStrainData_df['Average strain Min'][0] = sum_strainMin/maxCycle
maxMinStressStrainData_df['Average strain amplitude'][0] = sum_strainAmplitude/maxCycle
maxMinStressStrainData_df['Average mean strain'][0] = sum_meanStrain/maxCycle

#==============================================================================
# write to file
#==============================================================================

maxMinStressStrainData_df.to_csv(writeFile_maxMinDataWithStressStrainAndTheirAverageValue,sep=';',index=False)

print 'Finish'
