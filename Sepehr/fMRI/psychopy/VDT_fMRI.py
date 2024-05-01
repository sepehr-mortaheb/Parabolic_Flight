
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --- Import packages ---
from psychopy import plugins
plugins.activatePlugins()
from psychopy import gui, visual, core, data, logging
from psychopy.constants import (NOT_STARTED, STARTED, PAUSED, FINISHED, priority)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding
import psychopy.iohub as io
from psychopy.hardware import keyboard
import pandas as pd
import os.path as op
from functions_fMRI import *
import serial

################################################################################

# Experiment Specifications 

## SET THE FOLLOWING PARAMETERS
subj_name = 'test1'
degree = '2.5'
seq = ['main']
initial_seq = 1

trig_box = 'keyboard' # 'serial'

## THESE ARE FIXED VARIABLES
img_dir = './images_eeg'
exl_dir = './'
BG_color = 'grey'
psychopyVersion = '2023.2.3'
expName = 'VDT'





for parad in range(initial_seq-1, len(seq)):
    paradigm = seq[parad]


    initial_run = 1

    for loop in range(initial_run, 6): 
        ImageListCreator(paradigm, degree, BG_color, img_dir, exl_dir)  
        expInfo = {
            'participant': f"sub-{subj_name}",
            'session': f"ses-{parad+1}{paradigm}",
            'run': f"run-{loop}",
            'date': data.getDateStr(),  # add a simple timestamp
            'expName': expName,
            'psychopyVersion': psychopyVersion,
            'BG_color': BG_color
        }
        expInfo = showExpInfoDlg(expInfo=expInfo)
        thisExp = setupData(expInfo=expInfo)
        logFile = setupLogging(filename=thisExp.dataFileName)
        win = setupWindow(expInfo=expInfo)
        inputs = setupInputs(expInfo=expInfo, thisExp=thisExp, win=win)

        if trig_box == 'keyboard':
            count = 0
            while count < 5:
                char = input("Press 't' to continue: ")
                if char.lower() == 't':
                    count += 1
        elif trig_box == 'serial':
            ser = serial.Serial('COM1', 9600)
            count = 0

            while count < 5:
                # Read a single character from the serial port
                char = ser.read().decode('utf-8')
                if char.lower() == 't':
                    count += 1
            ser.close()
        
        run(
            expInfo=expInfo, 
            thisExp=thisExp, 
            win=win, 
            inputs=inputs
        )
        saveData(thisExp=thisExp)

quit(thisExp=thisExp, win=win, inputs=inputs)


################################################################################




