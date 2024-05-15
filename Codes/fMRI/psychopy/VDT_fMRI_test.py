#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --- Import packages ---
import os
from functions_fMRI import *
from psychopy import visual, core, logging, event
from psychopy.hardware import keyboard
from multiprocessing import Process, Queue
import numpy as np 

def key_press_listener(q, timer):
    """Function to listen for key presses."""
    while True:
        keys = event.getKeys(['a', 'b', 'c', 'e'])
        if keys:
            q.put((keys[0], timer.getTime()))


################################################################################
if __name__ == '__main__':

# Subject Information 
    # Subject name 
    sub_name = 'sub-test01'
    tilt_degree = 2.5

    # Subject-Specific Block Order  
    ## It is better to give the order manually. If something happens during the 
    ## the acquisition, it is not necessary to start from the beginning, as we 
    ## we already now the order of the blocks. 
    block_order = ['M', 'C', 'C', 'M', 'M', 'C'] # M: main, C: control

    jitter = 0.1 #seconds 

    ################################################################################
    # Psychopy Variables Initialization 
        # Window setup 
    win = visual.Window(
        size=[1920, 1080], fullscr=True, screen=1,
        winType='pyglet', allowStencil=False,
        monitor='testMonitor', color=[0, 0, 0], colorSpace='rgb', 
        backgroundFit='none',
        blendMode='avg', useFBO=True,
        units='height'
    )

        # Logging events 
    log_file = f'log_{sub_name}.log'
    logging.LogFile(log_file, level=logging.INFO, filemode='w')

        # Tiemr
    GlobalTimer = core.Clock()

        # Parallel keyboard monitoring 
    q = Queue()
    listener_process = Process(target=key_press_listener, args=(q, GlobalTimer))
    listener_process.daemon = True
    listener_process.start()


        # Keyboard 
    kb = keyboard.Keyboard()
    ################################################################################
    # Stimuli and other variables
        # number of initial triggers from the scanner 
    n_triggers = 5 
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

    ################################################################################
    # Acquisition 
    logging.log(msg=f"The block order is {block_order}", level=logging.INFO)
    logging.log(msg=f"The elips tilt degree is {tilt_degree}", level=logging.INFO)

    # Waiting for the scanner triggers 
    text_trigger.draw()
    win.flip()
    trigger_times = wait_for_trigger(n_triggers, GlobalTimer)

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
            logging.log(msg=f"Start of the main block {count} at {GlobalTimer.getTime()}", 
                        level=logging.INFO
                    )
            
            std_idx = np.where(np.array(stim_order) == 'std')[0]
            np.random.shuffle(std_idx)
            for idx in std_idx[0:35]:
                stim_order[idx] = 'std_cw'
            for idx in std_idx[35:70]:
                stim_order[idx] = 'std_ccw'

            for stim in stim_order:
                if stim == 'dev':
                    image = stim_images['VWhite']
                elif stim == 'std_cw':
                    image = stim_images['CWWhite']
                elif stim == 'std_ccw':
                    image = stim_images['CCWWhite']
                
                logging.log(msg=f"Trial {stim} at {GlobalTimer.getTime()}", 
                            level=logging.INFO
                        )
                image.draw()
                win.flip()
                timer = core.Clock()
                onset_time = timer.getTime()
                while timer.getTime() < 1:
                # Check for any key presses
                    keys = kb.getKeys(keyList=['a'])
                    if keys:
                        for key in keys:
                            logging.log(msg=f"Key {key} was pressed at {timer.getTime() - onset_time}", 
                                        level=logging.INFO
                                    )
                            print(f"Key {key} was pressed at {timer.getTime() - onset_time}")

                win.flip()
                while timer.getTime() < 2:
                # Check for any key presses
                    keys = kb.getKeys(keyList=['a'])
                    if keys:
                        for key in keys:
                            logging.log(msg=f"Key {key} was pressed at {timer.getTime() - onset_time}", 
                                        level=logging.INFO
                                    )
                            print(f"Key {key} was pressed at {timer.getTime() - onset_time}")
            #main_block(stim_order, stim_images, win, GlobalTimer, kb, jitter)
            logging.log(msg=f"End of the main block {count} at {GlobalTimer.getTime()}", 
                        level=logging.INFO
                    )
        elif block == 'C':
            print(f"Running Block: {count} => Control")
            ref_yellow.draw()
            win.flip()
            core.wait(2)
            logging.log(msg=f"Start of the control block {count} at {GlobalTimer.getTime()}", 
                        level=logging.INFO
                    )
            control_block(stim_order, stim_images, win, GlobalTimer, kb, jitter)
            logging.log(msg=f"End of the control block {count} at {GlobalTimer.getTime()}", 
                        level=logging.INFO
                    )
        count += 1


    # Close the window
    win.close()

    ################################################################################




