# Parabolic Flight Project

This repository contains the codes related to the Oddball experiment, preprocessing, and the analysis of data in the Parabolic-Flight study. 

The Oddball task involves verticality detection. 
The cognitive task codes were written in `Python` using the `PSychopy` package. 

In all the following experiments, there are always two different blocks: 
  - Main
  - Control
    
In the `Main` block, participants are asked to respond to the verticality of the stimuli. However, in the `Control` block, participants are asked to respond to the color of the stimuli. 

## Behavioual

In the behavioral paradigm, the procedure is as follows: 
  - `Main` and `Control` blocks while the participant lays down.
  - `Main` and `Control` blocks while the participant sits down.
  - Applying tDCS
  - `Main` and `Control` blocks while the participant sits down.

The order of the blocks and possible positions are randomized for each participant. The session after the tDCS is always in the sit-down position. 

In each block, **270 stimuli** are presented **(60 deviant, 210 standard)**. 

To run the experiment, you need to run the `VDT_BEH.py` file in the `./Codes/Behavioural` directory.  

## EEG 

The EEG paradigm is designed to be used inside an airplane during a parabolic flight. 

It consists of **5 blocks (3 `Main` and 2 `Control`)**, presented in a randomized order for each participant, and each consisting of **5 runs**. In each run, **18 stimuli** are presented **(4 deviant, 14 standard)**.

To run the experiment, you need to run the `VDT_EEG.py` file in the `./Codes/EEG/task_codes` directory. 


## fMRI 
The fMRI paradigm is used in a 3T Siemens scanner with a repetition time of TR = 1 second. 

The paradigm consists of **20 blocks (10 `Main` and 10 `Control`)**, presented in a randomized order for each participant. Each block consists of a total of **18 trials: 4 deviant and 14 standard**. Each trial lasts 1 second. There is an inter-trial interval of 1 second accompanied by a random jitter. The jitters are produced in a pseudorandom manner in order to keep the length of the blocks consistent and equal to 36 seconds. The jitters are chosen from the range of -100ms to 100ms with 10ms steps in a way that they sum up to zero.


