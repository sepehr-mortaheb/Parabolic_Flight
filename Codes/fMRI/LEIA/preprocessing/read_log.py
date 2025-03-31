#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --- Import packages ---
import os.path as op
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
import pandas as pd 
from scipy.io import savemat, loadmat

###############################################################################
# --- Initialization --- 

# Initial Info 
data_dir = '/Users/sepehrmortaheb/MyDrive/LEIA/Projects/Parabolic-Flight/Data/fMRI/Campaign1_Oct2024/main/log_files'
subj = 'sub-C1P06_PRE'

# Reading the log file 
log_file = op.join(data_dir, subj, f"{subj}_log.log")
with open(log_file) as f:
    lines = f.readlines()

# Removing unnecessary characters in the lines 
lines = [l for l in lines if len(l.split('\n')[0].split('\t'))>=3]
lines = [l for l in lines if l.split('\t')[1]=='INFO ']
lines = [l.split('\n')[0].split('\t')[2].split(' ') for l in lines]
#lines = [l for l in lines if (l[1]!='t') & (l[1]!='lshift')]

# Find the reference initial time 
for l in lines: 
    if (l[0]=='Trigger') & (l[1]=='1'):
        t_start = np.double(l[3])
        break

################################################################################

# --- Block-Level Information ---  

# Extracting Block Info 
i = 0
b_onset_main = []
b_onset_cont = []
b_onset_silc = []
b_dur_main = []
b_dur_cont = []
b_dur_silc = []
for i in range(len(lines)):
    # Extracting main and control blocks information 
    if lines[i][0]=='Start':
        b_onset = np.double(lines[i+1][3]) - t_start
        b_name = lines[i][3]
        for j in range(i+1, len(lines)):
            if lines[j][0]=='End':
                b_offset = np.double(lines[j][7]) - t_start
                b_duration = b_offset - b_onset
                break
        if b_name == 'main':
            b_onset_main = b_onset_main + [b_onset]
            b_dur_main = b_dur_main + [b_duration]
        elif b_name == 'control':
            b_onset_cont = b_onset_cont + [b_onset]
            b_dur_cont = b_dur_cont + [b_duration]

    # Extracting silence block information 
    if lines[i][0]=='End':
        b_onset = np.double(lines[i][7]) - t_start
        for j in range(i+1, len(lines)):
            if lines[j][0]=='Start':
                b_offset = np.double(lines[j][7]) - t_start
                b_duration = b_offset - b_onset
                break

        b_onset_silc = b_onset_silc + [b_onset]
        b_dur_silc = b_dur_silc + [b_duration]
b_dur_silc[-1] = np.mean(np.array(b_dur_silc[0:-1])) # As we do not have the offset 
                                                     # time for the last silence, I 
                                                     # put the average duration of the 
                                                     # other silence blocks as the 
                                                     # duration of this block.

# Preparing the block information for saving as a mat file 
b_names = np.array(['main', 'control', 'silence'],  dtype=object)
b_onsets = np.array([np.array(b_onset_main).reshape((len(b_onset_main), 1)), 
                     np.array(b_onset_cont).reshape((len(b_onset_cont), 1)), 
                     np.array(b_onset_silc).reshape((len(b_onset_silc), 1))
                    ],  
                     dtype=object
                )
b_durs = np.array([np.array(b_dur_main).reshape((len(b_dur_main), 1)), 
                     np.array(b_dur_cont).reshape((len(b_dur_cont), 1)), 
                     np.array(b_dur_silc).reshape((len(b_dur_silc), 1))
                    ],  
                     dtype=object
                )

# Saving block information as a mat file
savemat(op.join(data_dir, subj, f"{subj}_block_info.mat"), 
        {'names': b_names, 'onsets':b_onsets, 'durations':b_durs}
    )

###############################################################################

# --- Trial-Level Information --- 

# Extracting Trial Info 
i = 0
t_onset_std = []
t_onset_dev_main = []
t_onset_dev_cont = []
t_dur_std = []
t_dur_dev_main = []
t_dur_dev_cont = []
for i in range(len(lines)):
    # Extracting main and control blocks information 
    if lines[i][0]=='Trial':
        onset = np.double(lines[i][3]) - t_start

        # The offset is a bit more complicated
        if lines[i+1][0]=='Trial': # If the next line is the next trial
            offset = np.double(lines[i+1][3]) - t_start
        elif lines[i+1][0]=='End': # If the next line is the end of the block
            offset = np.double(lines[i+1][7]) - t_start
        elif (lines[i+1][0]=='Key') & (lines[i+2][0]=='Trial'): 
            # If the next line is about a keypress and the one after that is another trial 
            offset = np.double(lines[i+2][3]) - t_start
        elif (lines[i+1][0]=='Key') & (lines[i+2][0]=='End'): 
            # If the next line is about a keypress and the one after that is the end of the block
            offset = np.double(lines[i+2][7]) - t_start

        duration = offset - onset

        # now check the trial type 
        if lines[i][1].startswith('m'): # This is in a main block 
            if lines[i][1].split('_')[1] == 'std': # This is a standard trial 
                t_onset_std = t_onset_std + [onset]
                t_dur_std = t_dur_std + [duration]
            elif lines[i][1].split('_')[1] == 'dev': # This is a deviant trial 
                t_onset_dev_main = t_onset_dev_main + [onset]
                t_dur_dev_main = t_dur_dev_main + [duration]

        if lines[i][1].startswith('c'): # This is in a control block
            if lines[i][1].split('_')[1] == 'std': # This is a standard trial 
                t_onset_std = t_onset_std + [onset]
                t_dur_std = t_dur_std + [duration]
            elif lines[i][1].split('_')[1] == 'dev': # This is a deviant trial 
                t_onset_dev_cont = t_onset_dev_cont + [onset]
                t_dur_dev_cont = t_dur_dev_cont + [duration]

# Preparing the trial information for saving as a mat file 
t_names = np.array(['std', 'dev_main', 'dev_cont'],  dtype=object)
t_onsets = np.array([np.array(t_onset_std).reshape((len(t_onset_std), 1)), 
                     np.array(t_onset_dev_main).reshape((len(t_onset_dev_main), 1)), 
                     np.array(t_onset_dev_cont).reshape((len(t_onset_dev_cont), 1))
                    ],  
                     dtype=object
                )
t_durs = np.array([np.array(t_dur_std).reshape((len(t_dur_std), 1)), 
                     np.array(t_dur_dev_main).reshape((len(t_dur_dev_main), 1)), 
                     np.array(t_dur_dev_cont).reshape((len(t_dur_dev_cont), 1))
                    ],  
                     dtype=object
                )

# Saving block information as a mat file
savemat(op.join(data_dir, subj, f"{subj}_trial_info.mat"), 
        {'names': t_names, 'onsets':t_onsets, 'durations':t_durs}
    )

################################################################################

# --- Subject's Performance Measures --- 

# Confusion matrix for the main blocks 
m_conf_mat = np.zeros((2,2))
for i in range(len(lines)-1):
    if lines[i][0] == 'Trial':
        if lines[i][1].startswith('m_std'):
            if (lines[i+1][0]=='Trial') | (lines[i+1][0]=='End'): 
                m_conf_mat[0, 0] += 1
            elif (lines[i+1][0]=='Key') | (lines[i+1][0]=='Keypress:'):
                m_conf_mat[0, 1] += 1
        elif lines[i][1].startswith('m_dev'):
            if (lines[i+1][0]=='Trial') | (lines[i+1][0]=='End'): 
                m_conf_mat[1, 0] += 1
            elif (lines[i+1][0]=='Key') | (lines[i+1][0]=='Keypress:'):
                m_conf_mat[1, 1] += 1
m_TN = m_conf_mat[0, 0]
m_TP = m_conf_mat[1, 1]
m_FP = m_conf_mat[0, 1]
m_FN = m_conf_mat[1, 0]
m_acc = np.round((m_TP + m_TN) / (m_TP + m_TN + m_FP + m_FN)*100, 2)
m_sen = np.round((m_TP) / (m_TP + m_FN)*100, 2)
m_spc = np.round((m_TN) / (m_TN + m_FP)*100, 2)
m_bacc = np.round((m_sen + m_spc)/2, 2)

# Confusion matrix for the control blocks 
c_conf_mat = np.zeros((2,2))
for i in range(len(lines)-1):
    if lines[i][0] == 'Trial':
        if lines[i][1].startswith('c_std'):
            if (lines[i+1][0]=='Trial') | (lines[i+1][0]=='End'): 
                c_conf_mat[0, 0] += 1
            elif (lines[i+1][0]=='Key') | (lines[i+1][0]=='Keypress:'):
                c_conf_mat[0, 1] += 1
        elif lines[i][1].startswith('c_dev'):
            if (lines[i+1][0]=='Trial') | (lines[i+1][0]=='End'): 
                c_conf_mat[1, 0] += 1
            elif (lines[i+1][0]=='Key') | (lines[i+1][0]=='Keypress:'):
                c_conf_mat[1, 1] += 1
c_TN = c_conf_mat[0, 0]
c_TP = c_conf_mat[1, 1]
c_FP = c_conf_mat[0, 1]
c_FN = c_conf_mat[1, 0]
c_acc = np.round((c_TP + c_TN) / (c_TP + c_TN + c_FP + c_FN)*100, 2)
c_sen = np.round((c_TP) / (c_TP + c_FN)*100, 2)
c_spc = np.round((c_TN) / (c_TN + c_FP)*100, 2)
c_bacc = np.round((c_sen + c_spc)/2, 2)

df_perf = pd.DataFrame(
    {
        'block': ['main', 'control'],
        'TN': [m_TN, c_TN],
        'TP': [m_TP, c_TP],
        'FP': [m_FP, c_FP],
        'FN': [m_FN, c_FN],
        'ACC': [m_acc, c_acc],
        'SENS': [m_sen, c_sen],
        'SPEC': [m_spc, c_spc],
        'Balanced_ACC':[m_bacc, c_bacc]
    }
)



# Reaction Times 
df = pd.DataFrame([])

for i in range(len(lines)-1):
    tmpdf = pd.DataFrame([])
    if lines[i][0] == 'Trial':
        if lines[i][1].startswith('m_dev'):
            if lines[i+1][0]=='Key':
                rt = np.double(lines[i+1][9])
                tmpdf['rt'] = [rt]
                tmpdf['block'] = ['main']
            elif lines[i+1][0]=='Keypress:':
                rt = np.double(lines[i+2][9])
                tmpdf['rt'] = [rt]
                tmpdf['block'] = ['main']
        elif lines[i][1].startswith('c_dev'):
            if lines[i+1][0]=='Key':
                rt = np.double(lines[i+1][9])
                tmpdf['rt'] = [rt]
                tmpdf['block'] = ['control']
            elif lines[i+1][0]=='Keypress:':
                rt = np.double(lines[i+2][9])
                tmpdf['rt'] = [rt]
                tmpdf['block'] = ['control']
    df = pd.concat((df, tmpdf), ignore_index=True)

df.to_csv(op.join(data_dir, subj, f"{subj}_RT.csv"))


df_perf['RT'] = [np.mean(df[df.block=='main']['rt']), 
                 np.mean(df[df.block=='control']['rt'])
                ]
df_perf.to_csv(op.join(data_dir, subj, f"{subj}_Performance.csv"))

# Plotting Reaction Times Distributions
fig, ax = plt.subplots(1, 1, figsize=(7, 5))
sns.kdeplot(
   data=df, 
   x="rt", 
   hue="block",
   fill=True,
   #palette="crest",
   alpha=.5, 
   linewidth=2,
   ax=ax
)
ax.set_xlabel('Reaction Time (seconds)', size=15)
plt.savefig(op.join(data_dir, subj, f"{subj}_RT.png"), dpi=300)

# Converting the events files from SPM-friendly format to the BIDS-friendly format
block_info = loadmat(op.join(data_dir, subj, f'{subj}_block_info.mat'))
block_names = block_info['names'][0]
block_onsets = block_info['onsets'][0]
block_onsets = [list(np.squeeze(block_onsets[i])) for i in range(len(block_onsets))]
block_durations = block_info['durations'][0]
block_durations = [list(np.squeeze(block_durations[i])) for i in range(len(block_durations))]
block_names = [list(block_names[i])*len(block_onsets[i]) for i in range(len(block_names))]

trial_info = loadmat(op.join(data_dir, subj, f'{subj}_trial_info.mat'))
trial_names = trial_info['names'][0]
trial_onsets = trial_info['onsets'][0]
trial_onsets = [list(np.squeeze(trial_onsets[i])) for i in range(len(trial_onsets))]
trial_durations = trial_info['durations'][0]
trial_durations = [list(np.squeeze(trial_durations[i])) for i in range(len(trial_durations))]
trial_names = [list(trial_names[i])*len(trial_onsets[i]) for i in range(len(trial_names))]

df0 = pd.DataFrame({'trial_type':list(block_names[0]), 
                    'onset':list(block_onsets[0]), 
                    'duration':list(block_durations[0])})
df1 = pd.DataFrame({'trial_type':list(block_names[1]), 
                    'onset':list(block_onsets[1]), 
                    'duration':list(block_durations[1])})
df2 = pd.DataFrame({'trial_type':list(block_names[2]), 
                    'onset':list(block_onsets[2]), 
                    'duration':list(block_durations[2])})
df3 = pd.DataFrame({'trial_type':list(trial_names[0]), 
                    'onset':list(trial_onsets[0]), 
                    'duration':list(trial_durations[0])})
df4 = pd.DataFrame({'trial_type':list(trial_names[1]), 
                    'onset':list(trial_onsets[1]), 
                    'duration':list(trial_durations[1])})
df5 = pd.DataFrame({'trial_type':list(trial_names[2]), 
                    'onset':list(trial_onsets[2]), 
                    'duration':list(trial_durations[2])})

df = pd.concat((df0, df1, df2, df3, df4, df5), ignore_index=True)

df_final = df.sort_values(['onset', 'duration'], 
               ascending=[True, False]).reset_index()[['trial_type', 'onset', 'duration']]
for i in range(len(df_final)):
    if df_final.loc[i, 'trial_type'] == 'control':
        df_final.loc[i, 'trial_type'] = 'b_control'
    elif df_final.loc[i, 'trial_type'] == 'main':
        df_final.loc[i, 'trial_type'] = 'b_main'
    elif df_final.loc[i, 'trial_type'] == 'silence':
        df_final.loc[i, 'trial_type'] = 'b_silence'
    elif df_final.loc[i, 'trial_type'] == 'std':
        df_final.loc[i, 'trial_type'] = 't_std'
    elif df_final.loc[i, 'trial_type'] == 'dev_cont':
        df_final.loc[i, 'trial_type'] = 't_dev_cont'
    elif df_final.loc[i, 'trial_type'] == 'dev_main':
        df_final.loc[i, 'trial_type'] = 't_dev_main'

df_final.to_csv(op.join(data_dir, subj, f'{subj}_events.csv'))
