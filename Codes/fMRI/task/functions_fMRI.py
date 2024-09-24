from psychopy import core, event, logging 
from numpy.random import random
import numpy as np


def wait_for_trigger(n_triggers, timer):
    trigger_count = 0
    trigger_times = []
    
    while trigger_count < n_triggers:
        # Wait for key press
        key = event.waitKeys(keyList=['5'])
        
        # Record trigger time
        trigger_time = timer.getTime()
        trigger_times.append(trigger_time)
    
        # Print trigger time
        logging.log(msg="Trigger {} time: {}".format(trigger_count + 1, trigger_time), level=logging.INFO)
        print("Trigger", trigger_count + 1, "time:", trigger_time)
    
        trigger_count += 1

    return trigger_times

def stim_order_creator(paradigm_config):
    n_std = paradigm_config['n_std']
    n_dev = paradigm_config['n_dev']
    dev_dist = paradigm_config['dev_dist']
    initial_std = paradigm_config['initial_std']

    order = ['dev']*n_dev + ['std']*(n_std - initial_std - n_dev*dev_dist)
    order = np.random.permutation(order)
    out = []
    for stim in order: 
        if stim == 'dev':
            out = out + ['dev'] + ['std']*dev_dist
        elif stim == 'std':
            out = out + ['std']
    out = ['std']*initial_std + out

    return out

def xy_finder(N):
    if np.remainder(N, 2) == 0: # if N is even 
        xList = np.array(range(2, N, 2)) # also x should be even 
    else: # if N is odd
        xList = np.array(range(1, N, 2)) # also x should be odd
    diff = []
    for x in list(xList):
        diff = diff + [np.abs(N/2 - 1.5*x)]
        
    idx_min = np.argmin(np.array(diff))
    x = xList[idx_min]
    y = int((N - x) / 2)

    return x, y



def main_block(stim_order, stim_images, win, globalTimer, kb, paradigm_config):
    ## In the response box, the buttons send the following characters:
    ## green: c 
    ## red: e 
    ## blue: a 
    ## yellow: b 
    n_std = paradigm_config['n_std']
    n_dev = paradigm_config['n_dev']
    max_jitter = paradigm_config['iti_jitter_max']
    stim_dur = paradigm_config['stim_dur']
    iti = paradigm_config['iti']

    # Psudorandom jitter generation which sums to zero to keep the length 
    # of the blocks consistent 
    n_stim = n_std + n_dev
    possible_jitters = np.arange(0, max_jitter+0.01, 0.01)
    if np.remainder(n_stim, 2) == 0: 
        tmp = np.random.choice(possible_jitters, int(n_stim/2))
        jitter_list = np.hstack((tmp, -tmp))
        jitter_list = np.random.permutation(jitter_list)
    else:
        tmp = np.random.choice(possible_jitters, int((n_stim-1)/2))
        jitter_list = np.hstack((tmp, -tmp, 0))
        jitter_list = np.random.permutation(jitter_list)

    # making balanced clockwise and counterclockwise standard stimuli 
    std_idx = np.where(np.array(stim_order) == 'std')[0]
    np.random.shuffle(std_idx)
    for idx in std_idx[0:int(n_std/2)]:
        stim_order[idx] = 'std_cw'
    for idx in std_idx[int(n_std/2):n_std]:
        stim_order[idx] = 'std_ccw'

    # Stimuli presentation
    count = 0 # counter to read the jitter values 
    for stim in stim_order:
        if stim == 'dev':
            image = stim_images['VWhite']
        elif stim == 'std_cw':
            image = stim_images['CWWhite']
        elif stim == 'std_ccw':
            image = stim_images['CCWWhite']
        
        logging.log(msg=f"Trial m_{stim} at {globalTimer.getTime()}", 
                    level=logging.INFO
                )
        image.draw()
        win.flip()
        timer = core.Clock()
        onset_time = timer.getTime()
        while timer.getTime() < stim_dur:
        # Check for any key presses during the image presentation
            ks = kb.getKeys(keyList=['1', '2', '3', '4', '6', '7', '8', '9'])
            if ks:
                for key in ks:
                    logging.log(msg=f"Key {key.name} was pressed with a reaction time of {timer.getTime() - onset_time} seconds!", 
                                level=logging.INFO
                            )
                    print(f"Key {key.name} was pressed with a reaction time of {timer.getTime() - onset_time} seconds!")

        win.flip()
        jitter = jitter_list[count]
        while timer.getTime() < stim_dur + iti + jitter:
        # Check for any key presses during the inter-trial interval 
            ks = kb.getKeys(keyList=['1', '2', '3', '4', '6', '7', '8', '9'])
            if ks:
                for key in ks:
                    logging.log(msg=f"Key {key.name} was pressed with a reaction time of {timer.getTime() - onset_time} seconds!", 
                                level=logging.INFO
                            )
                    print(f"Key {key.name} was pressed with a reaction time of {timer.getTime() - onset_time} seconds!")
        count = count+1

        

def control_block(stim_order, stim_images, win, globalTimer, kb, paradigm_config):
    ## In the response box, the buttons send the following characters:
    ## green: c 
    ## red: e 
    ## blue: a 
    ## yellow: b 
    n_std = paradigm_config['n_std']
    n_dev = paradigm_config['n_dev']
    max_jitter = paradigm_config['iti_jitter_max']
    stim_dur = paradigm_config['stim_dur']
    iti = paradigm_config['iti']

    # Psudorandom jitter generation which sums to zero to keep the length 
    # of the blocks consistent 
    n_stim = n_std + n_dev
    possible_jitters = np.arange(0, max_jitter+0.01, 0.01)
    if np.remainder(n_stim, 2) == 0: 
        tmp = np.random.choice(possible_jitters, int(n_stim/2))
        jitter_list = np.hstack((tmp, -tmp))
        jitter_list = np.random.permutation(jitter_list)
    else:
        tmp = np.random.choice(possible_jitters, int((n_stim-1)/2))
        jitter_list = np.hstack((tmp, -tmp, 0))
        jitter_list = np.random.permutation(jitter_list)

    std_idx = np.where(np.array(stim_order) == 'std')[0]
    dev_idx = np.where(np.array(stim_order) == 'dev')[0]
    np.random.shuffle(std_idx)
    np.random.shuffle(dev_idx)

    # making balanced clockwise and counterclockwise standard and deviant stimuli 
    x_std, y_std = xy_finder(n_std)
    for idx in std_idx[0:x_std]:
        stim_order[idx] = 'std_v'
    for idx in std_idx[x_std:x_std+y_std]:
        stim_order[idx] = 'std_cw'
    for idx in std_idx[x_std+y_std:n_std]:
        stim_order[idx] = 'std_ccw'

    x_dev, y_dev = xy_finder(n_dev)
    for idx in dev_idx[0:x_dev]:
        stim_order[idx] = 'dev_v'
    for idx in dev_idx[x_dev:x_dev+y_dev]:
        stim_order[idx] = 'dev_cw'
    for idx in dev_idx[x_dev+y_dev:n_dev]:
        stim_order[idx] = 'dev_ccw'

    # Stimuli Presentation
    count = 0 # counter to read the jitter values 
    for stim in stim_order:
        if stim == 'std_v':
            image = stim_images['VWhite']
        elif stim == 'std_cw':
            image = stim_images['CWWhite']
        elif stim == 'std_ccw':
            image = stim_images['CCWWhite']
        elif stim == 'dev_v':
            image = stim_images['VYellow']
        elif stim == 'dev_cw':
            image = stim_images['CWYellow']
        elif stim == 'dev_ccw':
            image = stim_images['CCWYellow']

        logging.log(msg=f"Trial c_{stim} at {globalTimer.getTime()}", 
                    level=logging.INFO
                )
        image.draw()
        win.flip()
        timer = core.Clock()
        onset_time = timer.getTime()
        while timer.getTime() < stim_dur:
        # Check for any key presses during the image presentation
            keys = kb.getKeys(keyList=['1', '2', '3', '4', '6', '7', '8', '9'])
            if keys:
                for key in keys:
                    logging.log(msg=f"Key {key.name} was pressed with a reaction time of {timer.getTime() - onset_time} seconds!", 
                                level=logging.INFO
                            )
                    print(f"Key {key.name} was pressed with a reaction time of {timer.getTime() - onset_time} seconds!")

        win.flip()
        jitter = jitter_list[count]
        while timer.getTime() < stim_dur + iti + jitter:
        # Check for any key presses during the inter-trial interval 
            keys = kb.getKeys(keyList=['1', '2', '3', '4', '6', '7', '8', '9'])
            if keys:
                for key in keys:
                    logging.log(msg=f"Key {key.name} was pressed with a reaction time of {timer.getTime() - onset_time} seconds!", 
                                level=logging.INFO
                            )
                    print(f"Key {key.name} was pressed with a reaction time of {timer.getTime() - onset_time} seconds!")
        count = count + 1
    



    