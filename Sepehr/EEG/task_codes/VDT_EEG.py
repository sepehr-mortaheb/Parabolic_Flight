
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
from functions import *

################################################################################

# Experiment Specifications 

subj_name = 'septest'
degree = '2.5'
paradigm = 'main' # 'main', 'control'
BG_color = 'grey'
initial_run = 1

img_dir = './images'
exl_dir = './'

psychopyVersion = '2023.2.3'
expName = 'VDT'

for loop in range(initial_run, 16): 
    ImageListCreator(paradigm, degree, BG_color, img_dir, exl_dir)  
    expInfo = {
        'participant': f"sub-{subj_name}",
        'session': f"ses-{paradigm}",
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
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win, 
        inputs=inputs
    )
    saveData(thisExp=thisExp)

quit(thisExp=thisExp, win=win, inputs=inputs)


################################################################################




