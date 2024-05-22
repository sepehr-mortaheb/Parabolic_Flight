#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --- Import packages ---
import os
import numpy as np 
import os.path as op
from functions_fMRI import *
from psychopy import visual, core, logging, event, gui
from psychopy.hardware import keyboard

################################################################################

# Subject Information 
# Subject name 
sub_name = 'SM-test'
tilt_degree = 1.5  

# Subject-Specific Block Order  
## It is better to give the order manually. If something happens during the 
## the acquisition, it is not necessary to start from the beginning, as we 
## we already now the order of the blocks. 

################################################################################

paradigm_type = 2 # 1: 6 long blocks, 3 main and 3 control 
                  # 2: 20 short blocks, 10 main and 10 control

# Paradigm Information 
if paradigm_type == 1:
    ## Subject-Specific Block Order  
    ## It is better to give the order manually. If something happens during the 
    ## the acquisition, it is not necessary to start from the beginning, as we 
    ## we already now the order of the blocks. 
    block_order = ['M', 'C', 'C', 'M', 'M', 'C'] # M: main, C: control
    n_blocks = len(block_order)
    n_dev = 20 # number of deviant stimuli per block 
    n_std = 70 # number of standard stimuli per block
elif paradigm_type == 2: 
    ## Subject-Specific Block Order  
    ## It is better to give the order manually. If something happens during the 
    ## the acquisition, it is not necessary to start from the beginning, as we 
    ## we already now the order of the blocks. 
    block_order = ['C', 'M', 'M', 'C', 'C', 'C', 'C', 'M', 'C', 'M', 'M', 'C', 'C',
                   'M', 'M', 'C', 'M', 'M', 'C', 'M'] # M: main, C: control
    n_blocks = len(block_order)
    n_dev = 4 # number of deviant stimuli per block 
    n_std = 14 # number of standard stimuli per block

# Other parameters are the same in both paradigms:
dev_dist = 2 # minimum distant between deviant stimuli 
initial_std = 2 # number of standard stimuli at start of the block 
ref_dur = 2 # duration of the reference image at the beginning of each block in seconds 
iti_jitter_max = 0.1 # max jitter for the inter-trial interval in seconds
stim_dur = 1 # duration of the stimulus image in seconds 
iti = 1 # inter-trial interval
ibi = 10 # inter-block interval (rest periods) in seconds 

paradigm_config = {
    'n_blocks': n_blocks,
    'n_dev': n_dev,
    'n_std': n_std,
    'dev_dist': dev_dist,
    'initial_std': initial_std,
    'ref_dur': ref_dur, 
    'iti_jitter_max': iti_jitter_max,
    'stim_dur': stim_dur,
    'iti': iti,
    'ibi': ibi
}

################################################################################
# Psychopy Variables Initialization 

# Logging events 
log_dir = f'./data/sub-{sub_name}'
    # Check if the directory already exists:
if op.isdir(log_dir) == False: # The directory does not exist
    os.makedirs(log_dir) # So, creat it. 
    log_file = op.join(log_dir, f'sub-{sub_name}_log.log')
    logging.LogFile(
        log_file, 
        level=logging.INFO, 
        filemode='w'
    )
elif op.isdir(log_dir) == True: # The directory already exists 
   log_file = op.join(log_dir, f'sub-{sub_name}_log.log')
   if op.exists(log_file) == True: # The log file also exists 
       raise ValueError("The log file already exists in this directory!")
   else: # So, the log file does not exist
       logging.LogFile(
        log_file, 
        level=logging.INFO, 
        filemode='w'
    )
       

    # Window setup 
win = visual.Window(
    size=[1920, 1080],
    fullscr=True,
    screen=1,
    winType='pyglet',
    allowStencil=False,
    allowGUI=False,
    monitor='testMonitor',
    color=[0, 0, 0],
    colorSpace='rgb',
    backgroundFit='contain',
    blendMode='avg', 
    useFBO=True,
    units='height'
)
win.winHandle.maximize()
win.winHandle.activate()

    # Tiemr
GlobalTimer = core.Clock()

    # Keyboard 
kb = keyboard.Keyboard()
################################################################################
# Stimuli and other variables
    # number of initial triggers from the scanner 
n_triggers = 5 

    # Text Stimuli Variables 
text_trigger = visual.TextStim(win, text="Waiting for the scanner triggers ...", color="white")
text_trigger.size = (0.2, 0.05)
text_rest = visual.TextStim(win, text="End of the block. \n (Please do not move!)", color="white")
text_rest.size = (0.2, 0.05)
text_start = visual.TextStim(win, text="Whenever you are ready\n press a button to start. ", color="white")
text_start.size = (0.2, 0.05)
text_end = visual.TextStim(win, text="End of the Experiment!", color="white")
text_end.size = (0.2, 0.05)


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

################################################################################
# Acquisition Codes 
logging.log(msg=f"The block order is {block_order}", level=logging.INFO)
logging.log(msg=f"The elips tilt degree is {tilt_degree}", level=logging.INFO)

    # Waiting for the participant to start the task 
while True: 
    text_start.draw()
    win.flip()
    keys = kb.getKeys(keyList=['a', 'b', 'c', 'e'])
    if keys:
        core.wait(0.5)
        break

    # Waiting for the scanner triggers 
text_trigger.draw()
win.flip()
win.mouseVisible = False
trigger_times = wait_for_trigger(n_triggers, GlobalTimer)

    # Start of the task 
for count in range(n_blocks):
    block = block_order[count]
    stim_order = stim_order_creator(paradigm_config)
    if block == 'M':
        logging.log(msg=f"Start of the main block {count+1} at {GlobalTimer.getTime()}", 
                    level=logging.INFO
                )
        print(f"Running Block: {count+1} => Main")

        # Showing the Reference Image 
        ref_white.draw()
        win.flip()
        core.wait(ref_dur)

        # start of the block 
        main_block(stim_order, stim_images, win, GlobalTimer, kb, paradigm_config)
        logging.log(msg=f"End of the main block {count+1} at {GlobalTimer.getTime()}", 
                    level=logging.INFO
                )
        print(f"End of block! Rest period!")
        # Rest period 
        text_rest.draw()
        win.flip()
        core.wait(ibi)


    elif block == 'C':
        logging.log(msg=f"Start of the control block {count+1} at {GlobalTimer.getTime()}", 
                    level=logging.INFO
                )
        print(f"Running Block: {count+1} => Control")

        # Showing the Reference Image 
        ref_yellow.draw()
        win.flip()
        core.wait(ref_dur)
        
        # start of the block
        control_block(stim_order, stim_images, win, GlobalTimer, kb, paradigm_config)
        logging.log(msg=f"End of the control block {count+1} at {GlobalTimer.getTime()}", 
                    level=logging.INFO
                )
        print(f"End of block! Rest period!")
        # Rest period 
        text_rest.draw()
        win.flip()
        core.wait(ibi)

# End of the Experiment
text_end.draw()
win.flip()
core.wait(2)
# Close the window
win.close()

################################################################################




