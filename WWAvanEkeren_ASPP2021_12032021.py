# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 18:49:22 2021

@author: wesva399
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from os import listdir

'''Open Landt file function definition'''
def open_land_file(file_name):
    file_name = '../Cycling/Landt/LHCE/1.5M LiFSI in TEP_BTFE210210_007_3.xls'
    xl = pd.ExcelFile(file_name)
    record_df=pd.read_excel(xl, sheet_name='Record', header=0)
    return record_df

'''Sets file name which is used as name to save the file'''
file_name = '../Cycling/Landt/LHCE/1.5M LiFSI in TEP_BTFE210210_007_3.xls'
file_name2 = file_name[22:-3]
file_name2

'''Open Landt file'''
open_land_file('../Cycling/Landt/LHCE/1.5M LiFSI in TEP_BTFE210210_007_3.xls')


file_name = '../Cycling/Landt/LHCE/1.5M LiFSI in TEP_BTFE210210_007_3.xls'
xl = pd.ExcelFile(file_name)
record_df=pd.read_excel(xl, sheet_name='Record', header=0)
sheet_list=xl.sheet_names
list_columns=record_df.columns
list_columns

record_df_list=[pd.read_excel(xl,sheet_name=x ,header=None,names=list_columns) for x in sheet_list if ('Record' in x) and (x!='Record')]
record_df_list

record_df=[record_df]+record_df_list
record_df

record_df=pd.concat(record_df,ignore_index=True)
record_df

state_list=record_df['State'].values
state_list

columns=record_df.columns
columns

def identify_cycle_sequence(start_mode):
    
    if 'Rate' in start_mode:
        sequence_list=['C_Rate','D_Rate']
    else:
        sequence_list=['C_CC','D_CC']
        
    if start_mode[0]=='D':
        sequence_list=[x for x in reversed(sequence_list)]
    return sequence_list

cycle_index_list=[None]*len(state_list)
#indentify initial_rest
cycle_start=0
if state_list[0]=='R':
    for x in range(len(state_list)):
        if state_list[x] != 'R':
            cycle_start=x
            break
        else:
            cycle_index_list[x]=0
else:
    cycle_start=0
print()
squence_list=identify_cycle_sequence(state_list[cycle_start])
cycle=1
sequence_index=0
for x in range(cycle_start,len(state_list)):
    if (state_list[x] != squence_list[sequence_index]) and (sequence_index==0):
        sequence_index+=1
    elif (state_list[x] == squence_list[0]) and (sequence_index==1):
        cycle+=1        
        sequence_index=0
                    
    cycle_index_list[x]=cycle

cycle_index_list[x]

record_df['Cycle']=cycle_index_list
del cycle_index_list
record_df

C_D_R_list=[x[0] for x in state_list]
C_D_R_list

def create_standard_operation_list(C_D_R_list):
    step_operation_list=[None]*len(C_D_R_list)
    for x in range(len(C_D_R_list)):
        if C_D_R_list[x]=='R':
            step_operation_list[x]='R'
        elif C_D_R_list[x]=='C_Rate' or C_D_R_list[x]=='C_CC':
            step_operation_list[x]='CC-Chg'
        elif C_D_R_list[x]=='D_Rate' or C_D_R_list[x]=='D_CC':
            step_operation_list[x]='CC-Dchg'
        
    return step_operation_list

record_df['Step Operation']=create_standard_operation_list(list(state_list))
del state_list
record_df['C/DC/R']=C_D_R_list #create universal indicator for charge, discharge and rest. (should also account for CCCV stuff)
record_df
del C_D_R_list

sum_cycle_df=pd.read_excel(xl,sheet_name='Cycle',header=0)
sum_cycle_df=sum_cycle_df.rename(columns={"Index": "Cycle"})
sum_cycle_df

data_dict={'record':record_df,'sum_cycle':sum_cycle_df}
data_dict

sum_cycle_df_columns=sum_cycle_df.columns
print(list(sum_cycle_df_columns))

sum_cycle_df['Coulombic_Efficiency'] = np.where(sum_cycle_df['Charge-Cap/mAh'] > 0, (sum_cycle_df['Discharge-Cap/mAh']/sum_cycle_df['Charge-Cap/mAh'])*100, np.NaN)
sum_cycle_df['Energy_Efficiency'] = np.where(sum_cycle_df['Charge-Energy/mWh'] > 0, (sum_cycle_df['Discharge-Energy/mWh']/sum_cycle_df['Charge-Energy/mWh'])*100, np.NaN)
sum_cycle_df

'''Plot the Discharge and Charge Capacity vs Cycle number, Also for Coulombic Efficiency and Energy Efficiency'''
fig, ax = plt.subplots(1, 1)

ax.plot(sum_cycle_df['Cycle'], sum_cycle_df['Discharge-SCap/mAh/g'],'bv',label='Discharge capacity') 
ax.plot(sum_cycle_df['Cycle'], sum_cycle_df['Charge-SCap/mAh/g'], 'rv',label='Charge capacity')
    
ax.set_ylabel('Charge/Discharge Capacity (mAh/g)')
ax.set_xlabel('Cycle Index')
ax.set_ylim(0, 160)


ax2 = ax.twinx()
ax2.plot(sum_cycle_df['Cycle'], sum_cycle_df['Coulombic_Efficiency'],'^', c=(90/255,180/255,172/255), label='Coulumbic Efficiency')
ax2.plot(sum_cycle_df['Cycle'], sum_cycle_df['Energy_Efficiency'],'^', c=(216/255,179/255,101/255), label='Energy Efficiency')
ax2.set_xlabel('Cycle Index')
ax2.set_ylabel('Efficiency (%)')
ax2.set_ylim(50, 100)

ax2.tick_params(axis='y',direction='inout')   

#comment out if you want two separate legends
lines, labels = ax.get_legend_handles_labels()       
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='lower right')

#uncomment if you want two legends
# ax.legend(loc='upper left')
# ax2.legend(loc='lower right') 

ax.tick_params(axis='both',direction='inout')
fig.tight_layout()
fig.set_size_inches(1.61803398875*4, 4,forward=True)
plt.savefig('../Graphs/Galv/LHCE/'+file_name2+'DCC_CE_EE.png', transparent=True,dpi=500)    
plt.show()