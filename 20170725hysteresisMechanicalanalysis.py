# -*- coding: utf-8 -*-
"""
Created on Mon Aug 07 11:09:03 2017

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
readFile_firstCycle =  'Nr2_cycle1_1kN.csv'
#print 'Input the file name you want to write the after mechanical analysis data:'
writeFile_mechanicalAnalysisData = 'experimentHysteresisMechanicalAanalysis_40_0.99_40_0.99.csv'

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
dfOutput = pd.DataFrame(columns = ['Cycle','Stress Max MPa','Stress Min MPa','Stress Amplitude MPa','Stress Mean MPa','Strain Max','Strain Min','Strain Amplitude','Strain Mean', 'Tensile Elastic Modulus GPa','Compressive Elastic Modulus GPa','Yield Stress MPa','Elastic Strain','Plastic Strain','Anelastic Strain', 'Effective Stress MPa','Back Stress MPa'])

for cycle in range (1, maxCycle-1):
   print cycle
   loop=df[df.Zyklus==cycle]
   strainMax = loop['Strain'].max()
   strainMin = loop['Strain'].min()
   strainAmp = (strainMax - strainMin)/2
   strainMean = (strainMax + strainMin)/2
   stressMax = loop['Stress MPa'].max()
   stressMin = loop['Stress MPa'].min()
   stressAmp = (stressMax - stressMin)/2
   stressMean = (stressMax + stressMin)/2
#==============================================================================
# #  return the index of data of max strain
#==============================================================================
   maxStrainCount = loop.Strain[loop.Strain==strainMax].index.tolist()[0]
   minStrainCount = loop.Strain[loop.Strain==strainMin].index.tolist()[0]
#==============================================================================
# # regression the linear part, calculate tensile elastic modulus
#==============================================================================
   eModulusSum_tensile = 0
   interceptSum_tensile = 0
   i = 0 #for emodulus Nr. count
   j = 0 # for fitting length shift over the fitting range
   fittingLength_tensile = 40 #set the minimum fitting length
   fittingStartPoint_tensile = maxStrainCount + 20#start fitting from the  maxStrainCount + 10
   fittingEndPoint_tensile = maxStrainCount + 65 #define the ftting end point at maxStrainCount+50, fitting range definition
   while fittingStartPoint_tensile + fittingLength_tensile <= fittingEndPoint_tensile and loop.index.max() >= fittingEndPoint_tensile:
       j = 0
       while fittingStartPoint_tensile+j+fittingLength_tensile <= fittingEndPoint_tensile:
           xx_tensile = loop.loc[fittingStartPoint_tensile+j:fittingStartPoint_tensile+j+fittingLength_tensile,:]['Strain']
           yy_tensile = loop.loc[fittingStartPoint_tensile+j:fittingStartPoint_tensile+j+fittingLength_tensile,:]['Stress MPa']
           slope_tensile, intercept_tensile, r_value_tensile, p_value_tensile, std_err_tensile = scipy.stats.linregress(xx_tensile,yy_tensile)
           eModulus_tensile = 0.001*slope_tensile 
           intercept_tensile = intercept_tensile
#           print r_value_tensile**2
#          print j
#          print eModulus_tensile
           j+=1
           if r_value_tensile**2 >= 0.99:
               eModulusSum_tensile+=eModulus_tensile
               interceptSum_tensile+=intercept_tensile
               i+=1
       fittingLength_tensile+=1
   try:
       eModulusAve_tensile = eModulusSum_tensile/i
       interceptAve_tensile = interceptSum_tensile/i
   except ZeroDivisionError:
       eModulusAve_tensile = None
       interceptAve_tensile = None
#       print 'Error' 
#   print eModulusAve_tensile
#==============================================================================
# #   regression the compressive part, calculate the compressive elastic modulus
#==============================================================================
   eModulusSum_compressive = 0
   interceptSum_compressive = 0
   h = 0 #for emodulus Nr. count
   k = 0 # for fitting length shift over the fitting range
   fittingLength_compressive = 40 #set the minimum fitting length
   fittingStartPoint_compressive = minStrainCount + 20#start fitting from the  maxStrainCount + 10
   fittingEndPoint_compressive = minStrainCount + 65 #define the ftting end point at maxStrainCount+50, fitting range definition
   while fittingStartPoint_compressive + fittingLength_compressive <= fittingEndPoint_compressive:
       k = 0
       while fittingStartPoint_compressive+k+fittingLength_compressive <= fittingEndPoint_compressive:
           xx_compressive = loop.loc[fittingStartPoint_compressive+k:fittingStartPoint_compressive+k+fittingLength_compressive,:]['Strain']
           yy_compressive = loop.loc[fittingStartPoint_compressive+k:fittingStartPoint_compressive+k+fittingLength_compressive,:]['Stress MPa']
           slope_compressive, intercept_compressive, r_value_compressive, p_value_compressive, std_err_compressive = scipy.stats.linregress(xx_compressive,yy_compressive)
           eModulus_compressive = 0.001*slope_compressive 
           intercept_compressive = intercept_compressive
 #          print r_value_compressive**2
 #          print k
 #          print eModulus_compressive
           k+=1
           if r_value_compressive**2 >= 0.99:
               eModulusSum_compressive+=eModulus_compressive
               interceptSum_compressive+=intercept_compressive
               h+=1
       fittingLength_compressive+=1
   try:
       eModulusAve_compressive = eModulusSum_compressive/h
       interceptAve_compressive = interceptSum_compressive/h
   except ZeroDivisionError:
       eModulusAve_compressive = None
#       print 'error'
#   print eModulusAve_compressive

#   for eModulusRegressionCount in range (10,len(loop.index)/4): 
#       if loop.index.max()< maxStrainCount+eModulusRegressionCount: #if the last cycle is not long enough will cause error report in the regression, if the loop length not enough, break
#           break
#       xx = loop.loc[fittingStartPoint:fittingStartPoint+eModulusRegressionCount, :]['Strain'] #try to get a series not df or will get error report 'NotImplementedError: Only 2-level MultiIndex are supported.'
#       yy = loop.loc[fittingStartPoint:fittingStartPoint+eModulusRegressionCount, :]['Stress MPa'] #set tge first fitting starting point is maxStrainCount+10 and end point is maxStrainCount+10
#       slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(xx,yy)
#       eModulus = 0.001*slope 
#       intercept = intercept
#       print r_value**2
#       eModulusRegressionCount+=1
#       if r_value**2>=0.999:
#           eModulusSum+=eModulus
#           i+=1
#           eModulusAve = eModulusSum/i
#       print eModulus
#       if i>1 and r_value**2<0.999:
#           break
#       print eModulusAve
# count the acquisition point per cycle
   counts=len(loop.index)
#==============================================================================
# # itterate each data point, yield stress, effective stress and back stress 
#==============================================================================
   for count in range(maxStrainCount+50,maxStrainCount+counts):  
       try:
           loop['Strain'][count]/((loop['Stress MPa'][count]-interceptAve_tensile)/(1000*eModulusAve_tensile))<(1-yieldStrain)
       except TypeError:
           stress_atYieldPoint = None
           yieldStress = None
       else:
           stress_atYieldPoint = loop['Stress MPa'][count]
           yieldStress = stressMax - stress_atYieldPoint
#          print 'yield point find'
#       if loop['Stress MPa'][count] < stressMean:
#           yieldStress = eModulusAve_tensile*yieldStrain
#           print 'yield point not find'
#           break
       try:
           (stressMax - stress_atYieldPoint)/2
       except TypeError:
           effectiveStress = None
           backStress = None
           break
       else:
           effectiveStress = (stressMax - stress_atYieldPoint)/2
           backStress = stressAmp - effectiveStress #instead of stressMax - effectiveStress, because case of with mean stress
           break
#==============================================================================
# # calculate elastic and plastic strain
#==============================================================================
   loop_right = loop[loop.Strain>strainMean]
   loop_left = loop[loop.Strain<strainMean] #divide one loop into left and right two parts
   index_right = abs(loop_right['Stress MPa']-stressMean).idxmin() #sort the indexs of left and right points most close to the mean stress
   index_left = abs(loop_left['Stress MPa']-stressMean).idxmin()
   plasticStrain = loop['Strain'][index_right] - loop['Strain'][index_left] #plastic strain defined as the strain axis between the right and left intersection points with loop
   try:
       0.001*stressAmp/eModulusAve_tensile
       0.001*stressAmp/eModulusAve_tensile
   except TypeError:
       if eModulusAve_compressive == None:
           if eModulusAve_tensile == None:
               elasticStrain = None
           else:
               elasticStrain_tensile = 0.001*stressAmp/eModulusAve_tensile
               elasticStrain = 2*elasticStrain_tensile
       if eModulusAve_tensile == None:
           if eModulusAve_compressive == None:
               elasticStrain = None
           else:
               elasticStrain_compressive = 0.001*stressAmp/eModulusAve_compressive
               elasticStrain = 2*elasticStrain_compressive              
   else:
       elasticStrain_tensile = 0.001*stressAmp/eModulusAve_tensile
       elasticStrain_compressive = 0.001*stressAmp/eModulusAve_compressive
       elasticStrain = elasticStrain_tensile + elasticStrain_compressive       
   try:
       anelasticStrain = 2*strainAmp - elasticStrain-plasticStrain
   except TypeError:
       anelasticStrain = None
   dfOutput.loc[len(dfOutput)] = [cycle,stressMax,stressMin,stressAmp,stressMean,strainMax,strainMin,strainAmp,strainMean,eModulusAve_tensile,eModulusAve_compressive,yieldStress,elasticStrain,plasticStrain,anelasticStrain,effectiveStress,backStress] #asign the vale to the dataframe
#==============================================================================
#  write dataframe to  csv
#==============================================================================
dfOutput.to_csv(writeFile_mechanicalAnalysisData, sep=';', index = False)

print 'finish'   
