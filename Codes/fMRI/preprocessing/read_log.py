#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --- Import packages ---
import os
import os.path as op
import numpy as np
from scipy.io import savemat

###############################################################################

# --- Initialization --- 

# Initial Info 
data_dir = '/Users/sepehrmortaheb/git_repo/Parabolic_Flight/Codes/fMRI/task/data'
subj = 'sub-SM-test'

# Reading the log file 
log_file = op.join(data_dir, subj, f"{subj}_log.log")
with open(log_file) as f:
    lines = f.readlines()

# Removing unnecessary characters in the lines 
lines = [l.split('\n')[0].split('\t')[2].split(' ') for l in lines]

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
        elif ((lines[i+1][0]=='Key') | (lines[i+1][0]=='Keypress:')) & (lines[i+3][0]=='Trial'): 
            # If the next line is about a keypress and the one after that is another trial 
            offset = np.double(lines[i+3][3]) - t_start
        elif ((lines[i+1][0]=='Key') | (lines[i+1][0]=='Keypress:')) & (lines[i+3][0]=='End'): 
            # If the next line is about a keypress and the one after that is the end of the block
            offset = np.double(lines[i+3][7]) - t_start

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
