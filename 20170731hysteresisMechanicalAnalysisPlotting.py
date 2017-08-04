# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 12:14:58 2017

@author: chen_w1
"""
#==============================================================================
# import the modules
#==============================================================================
import pandas as pd
import numpy as np
from pandas import DataFrame, read_csv,read_excel
import scipy
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

#==============================================================================
# read file
#==============================================================================
readFile_mechanicalAnalysisData = 'experimentHysteresisMechanicalAanalysis.csv'
df=pd.read_csv(readFile_mechanicalAnalysisData,sep=';')
#maximum stress
plt.figure(1)
#plt.subplot(321)
plt.title('Stress vs. Cycle')
plt.plot(df['Cycle'],df['Stress Max MPa'],'k-',label='Stress max')
plt.ylabel('Stress [MPa]')
plt.xlabel('Cycle [-]')
plt.ylim(239,240.5)
plt.xscale('log')
plt.legend(loc=3)

#minimum stress
#plt.subplot(322)
plt.figure(2)
plt.title('Stress vs. Cycle')
plt.plot(df['Cycle'],df['Stress Min MPa'],'r-',label='Stress min')
plt.ylabel('Stress [MPa]')
plt.xlabel('Cycle [-]')
plt.xscale('log')
plt.legend(loc=3)

#effective stress and back stress
#plt.subplot(323)
plt.figure(3)
plt.title('Stress vs. Cycle')
plt.plot(df['Cycle'],df['Back Stress MPa'],'b-',label='Back stress')
plt.plot(df['Cycle'],df['Effective Stress MPa'],'r-',label='Effective stress')
plt.ylabel('Stress [MPa]')
plt.xlabel('Cycle [-]')
plt.xscale('log')
plt.legend(loc='center left')

#back stress
#plt.subplot(324)
#plt.figure(4)
#plt.title('Stress vs. Cycle')
#plt.plot(df['Cycle'],df['Back Stress MPa'],'r-',label='Back stress')
#plt.ylabel('Stress [MPa]')
#plt.xlabel('Cycle [-]')
#plt.xscale('log')
#plt.legend(loc=3)

#strain amp, strain mean, srain max and min
#plt.subplot(325)
plt.figure(5)
strainMax = plt.subplot()
strainMin = plt.subplot()
strainMean = plt.subplot()
plt.title('Strain vs. Cycle')
strainMax.plot(df['Cycle'],df['Strain Max'],'k-',label='Strain max')
strainMin.plot(df['Cycle'],df['Strain Min'],'k--',label='Strain min')
strainMean.plot(df['Cycle'],df['Strain Mean'],'g-',label='Mean strain')
plt.ylabel('Strain [-]')
plt.xlabel('Cycle [-]')
plt.ylim(-0.005,0.010)
plt.xscale('log')
plt.legend(loc='upper left')

strainAmp = strainMax.twinx()
strainAmp.plot(df['Cycle'],df['Strain Amplitude'],'b-',label='Strain amplitude')
plt.ylabel('Strain [-]')
plt.xlabel('Cycle [-]')
plt.ylim(0,0.003)
plt.xscale('log')
plt.legend(loc='upper center')


#plastic and elastic strain
#plt.subplot(326)
plt.figure(6)
plt.title('Strain vs. Cycle')
plt.plot(df['Cycle'],df['Plastic Strain'],'k-',label='Plastic strain')
plt.plot(df['Cycle'],df['Elastic Strain'],'r-',label='Elastic strain')
plt.ylabel('Strain [-]')
plt.xlabel('Cycle [-]')
plt.ylim(0,0.002)
plt.xscale('log')
plt.legend(loc='upper left')

#elsatic modulus
plt.figure(7)
plt.subplot(211)
plt.title('Elastic Modulus vs. Cycle')
plt.plot(df['Cycle'],df['Elastic Modulus GPa'],'k-',label='Elastic modulus')
plt.ylabel('Elastic modulus [GPa]')
plt.xlabel('Cycle [-]')
plt.xscale('log')
plt.legend(loc=3)

plt.subplot(212)
plt.title('Stress vs. Cycle')
plt.plot(df['Cycle'],df['Yield Stress MPa'],'k-',label='Yield stress')
plt.ylabel('Yield stress [MPa]')
plt.xlabel('Cycle [-]')
plt.xscale('log')
plt.legend(loc=3)
plt.tight_layout()


plt.show()
