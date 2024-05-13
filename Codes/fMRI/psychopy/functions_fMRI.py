from psychopy import core, event, logging 
import pandas as pd 


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