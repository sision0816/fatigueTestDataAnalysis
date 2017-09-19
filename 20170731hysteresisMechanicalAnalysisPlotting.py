# -*- coding: utf-8 -*-
"""
Created on Wed Aug 02 15:45:24 2017

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
readFile_mechanicalAnalysisData = 'experimentStrainEnergyCalculationResult.csv'
df=pd.read_csv(readFile_mechanicalAnalysisData,sep=';')
#maximum stress
plt.figure(1)
#plt.subplot(321)
plt.title('Strain Energy vs. Cycle')
plt.plot(df['Cycle'],df['Total Cyclic Strain Energy_trapz MJ/m3'],'k-',label='Total strain energy')
plt.plot(df['Cycle'],df['Plastic Strain Energy_trapz MJ/m3'],'r-',label='Plastic strain energy')
plt.plot(df['Cycle'],df['Elastic Strain Energy MJ/m3'],'g-',label='Elastic strain energy')
plt.ylabel('Strain energy MJ/m^3')
plt.xlabel('Cycle [-]')
plt.ylim(0,4)
plt.xscale('log')
plt.legend(loc='best')

plt.show()

plt.figure(1)
#plt.subplot(321)
plt.title('Loop Shape Parameter vs. Cycle')
plt.plot(df['Cycle'],df['Loop Shape Parameter_trapz'],'k-',label='Loop shape parameter')
plt.ylabel('Loop shape parameter')
plt.xlabel('Cycle [-]')
plt.ylim(0,1)
plt.xscale('log')
plt.legend(loc='best')

plt.show()
