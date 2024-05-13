#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --- Import packages ---

from functions_fMRI import *
import serial
from psychopy import visual, core, event, logging 
import os
################################################################################


# Psychopy Variables Initialization 
win = visual.Window(
     size=[1920, 1080], fullscr=True, screen=1,
     winType='pyglet', allowStencil=False,
     monitor='testMonitor', color=[0, 0, 0], colorSpace='rgb', 
     backgroundFit='none',
     blendMode='avg', useFBO=True,
     units='height'
)
timer = core.Clock()
log_file = 'trigger_times.log'
logging.LogFile(log_file, level=logging.INFO, filemode='w')

# Stimuli and other variables 
n_triggers = 5 # number of initial triggers from the scanner 

    # Texts 
text_trigger = visual.TextStim(win, text="Waiting for the scanner triggers ...", color="white")
text_trigger.size = (0.3, 0.1)

    # Images 
ref_white = visual.ImageStim(
        win=win,
        name='ref_white', 
        image='./images_fMRI/Ref_white.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), size=(2,1),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
ref_yellow = visual.ImageStim(
        win=win,
        name='ref_yellow', 
        image='./images_fMRI/Ref_yellow.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), size=(2,1),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
bg = visual.ImageStim(
        win=win,
        name='bg', 
        image=f'./images_fMRI/grey_bg.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), size=(2, 1),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)



# Waiting for the scanner triggers 
text_trigger.draw()
win.flip()
trigger_times = wait_for_trigger(n_triggers, timer)


# Task codes 
## Loop to present the text stimulus 10 times
for _ in range(10):
    # Display the text stimulus
    ref_white.draw()
    win.flip()
    t = timer.getTime()
    logging.log(msg="Stimulus white time: {}".format(t), level=logging.INFO)
    print(timer.getTime())
    
    # Wait for 1 second
    core.wait(1)
    
    # Clear the screen
    win.flip()
    
    # Wait for 1 second (inter-stimulus interval)
    core.wait(1)

# Close the window
win.close()

################################################################################




