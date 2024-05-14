from psychopy import core, event, logging 
import numpy as np

def wait_for_trigger(n_triggers, timer):
    trigger_count = 0
    trigger_times = []
    
    while trigger_count < n_triggers:
        # Wait for key press
        key = event.waitKeys(keyList=['t'])
        
        # Record trigger time
        trigger_time = timer.getTime()
        trigger_times.append(trigger_time)
    
        # Print trigger time
        logging.log(msg="Trigger {} time: {}".format(trigger_count + 1, trigger_time), level=logging.INFO)
        print("Trigger", trigger_count + 1, "time:", trigger_time)
    
        trigger_count += 1

    return trigger_times

def stim_order_creator():
    order = ['dev']*20 + ['std']*28
    order = np.random.permutation(order)
    out = []
    for stim in order: 
        if stim == 'dev':
            out = out + ['dev', 'std', 'std']
        elif stim == 'std':
            out = out + ['std']
    out = ['std', 'std'] + out

    return out

def main_block(stim_order, stim_images, win, timer):
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

        logging.log(msg="Trial {} at {}".format(stim, timer.getTime()), level=logging.INFO)
        image.draw()
        win.flip()
        core.wait(1)
        win.flip()
        core.wait(1)
    