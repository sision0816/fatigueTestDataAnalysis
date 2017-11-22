# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 11:32:37 2017

@author: chen_w1
"""
import pandas as pd
import numpy as np
from pandas import DataFrame, read_csv,read_excel
import scipy
import scipy.stats

def partsBinding (n):# n is parts number
#==============================================================================
# input the read file name and write file name
#==============================================================================
    for i in range(1,n+1):
        print 'Type in the {}th part file name, including .csv'.format(i)
        globals()['readFile_timeSequence_part{}'.format(i)]  = input() #type in the parts file name with '' and .csv, it is very important
    print 'Type in the output file name, including .csv'
    writeFile_timeSequence_binded = input()
#==============================================================================
# read the csv data file into dataframe
#==============================================================================
    for j in range(1,n+1):
        globals()['df_part{}'.format(j)] = pd.read_csv(globals()['readFile_timeSequence_part{}'.format(j)],sep=';')
    df_binded = df_part1
#==============================================================================
# binding the parts dataframe together
#==============================================================================
    for k in range(2,n+1):
        timeCorrection_temp =  globals()['df_part{}'.format(k)]['Zeit s'][1]
        cycleNrCorrection_temp = globals()['df_part{}'.format(k)]['Zyklus'].min()
        globals()['df_part{}'.format(k)]['Zeit s'] = globals()['df_part{}'.format(k)]['Zeit s'] + timeCorrection_temp + globals()['df_part{}'.format(k-1)]['Zeit s'].max()
        globals()['df_part{}'.format(k)]['Zyklus'] = globals()['df_part{}'.format(k)]['Zyklus'] - cycleNrCorrection_temp + globals()['df_part{}'.format(k-1)]['Zyklus'].max() + 1
        df_binded = pd.concat([df_binded,globals()['df_part{}'.format(k)]],ignore_index=True)
#==============================================================================
# write the binded .csv file
#==============================================================================
    df_binded.to_csv(writeFile_timeSequence_binded, sep=';', index = False)

    print 'finish'   
    return;

        
    
        
