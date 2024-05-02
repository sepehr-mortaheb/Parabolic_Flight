#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --- Import packages ---

from functions_fMRI import *
import serial
from psychopy import visual, core
import os
################################################################################

win = visual.Window(
     size=[1920, 1080], fullscr=True, screen=1,
     winType='pyglet', allowStencil=False,
     monitor='testMonitor', color=[0, 0, 0], colorSpace='rgb', 
     backgroundFit='none',
     blendMode='avg', useFBO=True,
     units='height'
)
text_scan = visual.TextStim(win, text="Waiting for the scanner triggers ...", color="white")
text_stim = visual.TextStim(win, text="Hello", color="white")

text_scan.draw()
win.flip()

trig_box = 'keyboard'

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else: # Assume Unix-based system
    import termios
    import sys
    import tty
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


if trig_box == 'keyboard':
    #count = 0
    #while count < 5:
        #char = input("Press 't' to continue: ")
        #if char.lower() == 't':
            #count += 1
    count = 0
    while count < 5:
        char = getch()
        if char.lower() == 't':
            count += 1
            print("You pressed 't'.")
        else:
            print("You didn't press 't'.")


elif trig_box == 'serial':
    ser = serial.Serial('COM1', 9600)
    count = 0
    while count < 5:
        # Read a single character from the serial port
        char = ser.read().decode('utf-8')
        if char.lower() == 't':
            count += 1
            print("you pressed 't'.")

# Loop to present the text stimulus 10 times
for _ in range(10):
    # Display the text stimulus
    text_stim.draw()
    win.flip()
    
    # Wait for 1 second
    core.wait(1)
    
    # Clear the screen
    win.flip()
    
    # Wait for 1 second (inter-stimulus interval)
    core.wait(1)

# Close the window
win.close()

################################################################################




