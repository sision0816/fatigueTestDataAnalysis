# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 09:26:13 2017

@author: chen_w1
"""

import pandas as pd
import numpy as np
import scipy
from scipy import integrate
from pandas import DataFrame, read_csv,read_excel
#==============================================================================
# input the read file name and write file name
#==============================================================================
#print 'Input the file name you want to analysis:' 
readFile_timeSequence = 'SK200_40_experiment_timeData_binded.csv' # in with csv format and in list
#print 'Input the file name you want to read of hysteresisMechanicalAnalysis result:' 
readFile_hysteresisMechanicalAnalysis = 'experimentHysteresisMechanicalAanalysis_40_0.99_40_0.99.csv' # in with csv format and in list
#print 'Input the file name of first cycle:' 
readFile_firstCycle = 'SK200_40_cycle1_1kN.csv' 
#print 'Input the file name you want to write for the strain enenergy calculation result:'
writeFile_strainEnergyCalculationResult = 'experimentStrainEnergyCalculationResult.csv'

#==============================================================================
# read the csv data file into dataframe
#==============================================================================

df=pd.read_csv(readFile_timeSequence,sep=';')
mechanicalAnalysisData = pd.read_csv(readFile_hysteresisMechanicalAnalysis,sep=';')


#==============================================================================
# specimen and test parameters
#==============================================================================

firstCycleFile = pd.read_csv(readFile_firstCycle,sep=';')
extensormeterInitialValue = firstCycleFile['Sandner_1983 mm'][0]
crossSection = 58.905
gageLength = 15
#yieldStrain = 0.0005

#==============================================================================
# # Stress strain calculation and transfer to stress strain data
#==============================================================================

df['Stress MPa']=pow(10,3)*df['Kraft kN']/crossSection #Stress unite in MPa
df['Strain']=(df['Sandner_1983 mm']-extensormeterInitialValue)/(gageLength-extensormeterInitialValue)

#==============================================================================
# itterate each cycle and calculate the strain energy
#==============================================================================
# determine the largest cycle number
maxCycle=int(df['Zyklus'].max())
#maxCycle = 1000
# define the output dataframe of max min data
dfOutput = pd.DataFrame(columns = ['Cycle','Stress Max MPa','Stress Min MPa','Stress Amplitude MPa','Stress Mean MPa','Strain Max','Strain Min','Strain Amplitude','Strain Mean', 'Total Cyclic Strain Energy_simps MJ/m3','Plastic Strain Energy_simps MJ/m3', 'Total Cyclic Strain Energy_trapz MJ/m3','Plastic Strain Energy_trapz MJ/m3','Elastic Strain Energy MJ/m3','Loop Shape Parameter_simps','Loop Shape Parameter_trapz'])

for cycle in range (1, maxCycle-1):#the maxCycle-1 cycle may cause error in the integration
   if cycle in df['Zyklus'].values:
       print (cycle)
       loop=df[df.Zyklus==cycle]
       indexStrainMin = loop.Strain[loop.Strain==loop.Strain.min()].index.tolist()[0] #the index of the min strain
       indexStrainMax = loop.Strain[loop.Strain==loop.Strain.max()].index.tolist()[0] #the index of the max strain
       strainMax = loop['Strain'].max()
       strainMin = loop['Strain'].min()
       strainAmp = (strainMax - strainMin)/2
       strainMean = (strainMax + strainMin)/2
       stressMax = loop['Stress MPa'].max()
       stressMin = loop['Stress MPa'].min()
       stress_atStrainMin = loop['Stress MPa'][indexStrainMin]
       stress_atStrainMax = loop['Stress MPa'][indexStrainMax]
       stressAmp = (stressMax - stressMin)/2
       stressMean = (stressMax + stressMin)/2
       loop['Stress MPa'] = loop['Stress MPa'] - stressMin
       loop['Strain'] = loop['Strain'] - strainMin # shift the origin (0,0) of the coodination to (strainMin, stressMin)
       interval = 4*strainAmp/len(loop)#calculation the point interval alone strain axis
    #==============================================================================
    #  upper half hysteresis
    #==============================================================================
       yyUpperRight_array = loop.loc[: indexStrainMax,['Stress MPa']].values.transpose() #reduce the upper right section
       xxUpperRight_array = loop.loc[: indexStrainMax,['Strain']].values.transpose()
       yyUpperLeft_array = loop.loc[indexStrainMin:,['Stress MPa']].values.transpose() #reduce the Upper left section
       xxUpperLeft_array = loop.loc[indexStrainMin:,['Strain']].values.transpose()
    #==============================================================================
    #   lower half hysteresis
    #==============================================================================
       yylower_array = loop.loc[indexStrainMax:indexStrainMin,['Stress MPa']].values.transpose()#be care for may be negative values
       xxlower_array = loop.loc[indexStrainMax:indexStrainMin,['Strain']].values.transpose()
    #==============================================================================
    #  intgrate via simps
    #==============================================================================
       energy_upperRight_simps = scipy.integrate.simps(yyUpperRight_array,xxUpperRight_array,even='avg')
       energy_upperLeft_simps = scipy.integrate.simps(yyUpperLeft_array,xxUpperLeft_array,even='avg')
       energy_totalCyclicStrain_simps = energy_upperRight_simps + energy_upperLeft_simps # total cyclic strain energy
       energy_nonplasticStrain_simps = np.absolute(scipy.integrate.simps(np.absolute(yylower_array),np.absolute(xxlower_array),even='avg'))#the integration would be negative value, should get absolute value for area
       energy_plasticStrain_simps = energy_totalCyclicStrain_simps - energy_nonplasticStrain_simps
    #==============================================================================
    #    intgrate via trapz
    #==============================================================================
       energy_upperRight_trapz = scipy.integrate.trapz(yyUpperRight_array,xxUpperRight_array,axis=-1)
       energy_upperLeft_trapz = scipy.integrate.trapz(yyUpperLeft_array,xxUpperLeft_array,axis=-1)
       energy_totalCyclicStrain_trapz = energy_upperRight_trapz + energy_upperLeft_trapz # total cyclic strain energy
       energy_nonplasticStrain_trapz = np.absolute(scipy.integrate.trapz(np.absolute(yylower_array),np.absolute(xxlower_array),axis=-1))#the integration would be negative value, should get absolute value for area
       energy_plasticStrain_trapz = energy_totalCyclicStrain_trapz - energy_nonplasticStrain_trapz
    #==============================================================================
    #    elastic strain energy
    #==============================================================================
       try:
           energy_elasticStrain = mechanicalAnalysisData['Elastic Strain'][cycle]*stressAmp
       except TypeError:
           energy_elasticStrain = None
    #==============================================================================
    #    loop shape parameter
    #==============================================================================
       squareArea = (strainMax-strainMin)*(stressMax-stressMin)
       shapeParameter_simps = energy_plasticStrain_simps[0]/squareArea
       shapeParemeter_trapz = energy_plasticStrain_trapz[0]/squareArea
       #output the analysis result
       dfOutput.loc[len(dfOutput)] = [cycle,stressMax,stressMin,stressAmp,stressMean,strainMax,strainMin,strainAmp,strainMean,energy_totalCyclicStrain_simps[0],energy_plasticStrain_simps[0],energy_totalCyclicStrain_trapz[0],energy_plasticStrain_trapz[0],energy_elasticStrain,shapeParameter_simps,shapeParemeter_trapz]
       
#==============================================================================
#  write dataframe to  csv
#==============================================================================
dfOutput.to_csv(writeFile_strainEnergyCalculationResult, sep=';', index = False)

print ('finish')   
