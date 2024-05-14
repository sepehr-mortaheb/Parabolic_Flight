#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --- Import packages ---

from functions_fMRI import *
import serial
from psychopy import visual, core, logging 
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
tilt_degree = 2.5
n_triggers = 5 # number of initial triggers from the scanner 

    # Text Stimuli Variables 
text_trigger = visual.TextStim(win, text="Waiting for the scanner triggers ...", color="white")
text_trigger.size = (0.3, 0.1)

    # Image Stimuli Variables 
bg = visual.ImageStim(
        win=win,
        name='bg', 
        image=f'./images_fMRI/grey_bg.png', 
        size=(2, 1),
        interpolate=True
    )
ref_white = visual.ImageStim(
        win=win,
        name='ref_white', 
        image='./images_fMRI/Ref_white.png', 
        #size=(1,1),
        interpolate=True
    )
ref_yellow = visual.ImageStim(
        win=win,
        name='ref_yellow', 
        image='./images_fMRI/Ref_yellow.png', 
        #size=(1,1),
        interpolate=True
    )
CW_white = visual.ImageStim(
        win=win,
        name='cw_white', 
        image=f'./images_fMRI/Sphere_CW-{tilt_degree}_BG-grey_stim-white.png', 
        #size=(1,1),
        interpolate=True
    )
CW_yellow = visual.ImageStim(
        win=win,
        name='cw_yellow', 
        image=f'./images_fMRI/Sphere_CW-{tilt_degree}_BG-grey_stim-yellow.png', 
        #size=(1,1),
        interpolate=True
    )
CCW_white = visual.ImageStim(
        win=win,
        name='ccw_white', 
        image=f'./images_fMRI/Sphere_CCW-{tilt_degree}_BG-grey_stim-white.png', 
        #size=(1,1),
        interpolate=True
    )
CCW_yellow = visual.ImageStim(
        win=win,
        name='ccw_yellow', 
        image=f'./images_fMRI/Sphere_CCW-{tilt_degree}_BG-grey_stim-yellow.png', 
        #size=(1,1),
        interpolate=True
    )
V_white = visual.ImageStim(
        win=win,
        name='v_white', 
        image=f'./images_fMRI/Sphere_Ref_BG-grey_stim-white.png', 
        #size=(1,1),
        interpolate=True
    )
V_yellow = visual.ImageStim(
        win=win,
        name='v_yellow', 
        image=f'./images_fMRI/Sphere_Ref_BG-grey_stim-yellow.png', 
        #size=(1,1),
        interpolate=True
    )

stim_images = {
    'Background': bg,
    'WhiteRef': ref_white,
    'YellowRef': ref_yellow,
    'CWWhite': CW_white,
    'CCWWhite': CCW_white,
    'CWYellow': CW_yellow,
    'CCWYellow': CCW_yellow,
    'VWhite': V_white,
    'VYellow': V_yellow
}

# Task Initialization 

    # Block randomization 
    ## It is better to give the order manually. If something happens during the 
    ## the acquisition, it is not necessary to start from the beginning, as we 
    ## we already now the order of the blocks. 
block_order = ['M', 'C', 'C', 'M', 'M', 'C'] # M: main, C: control
logging.log(msg="The block order is {}".format(block_order), level=logging.INFO)


# Waiting for the scanner triggers 
text_trigger.draw()
win.flip()
trigger_times = wait_for_trigger(n_triggers, timer)


# Task codes 
## Loop to present the text stimulus 10 times
count = 1
for block in block_order:
    stim_order = stim_order_creator()
    if block == 'M':
        print(f"Running Block: {count} => Main")
        ref_white.draw()
        win.flip()
        core.wait(2)
        logging.log(msg="Start of the main block {} at {}".format(count, timer.getTime()), level=logging.INFO)
        main_block(stim_order, stim_images, win, timer)
        logging.log(msg="End of the main block {} at {}".format(count, timer.getTime()), level=logging.INFO)
    #elif block == 'C':
     #   logging.log(msg="Start of the control block {}: {}".format(count, timer.getTime()), level=logging.INFO)
      #  control_block(stim_order, stim_images, win)
    count += 1


# Close the window
win.close()

################################################################################




