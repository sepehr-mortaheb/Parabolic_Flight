
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER, priority)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding
import psychopy.iohub as io
from psychopy.hardware import keyboard
import pandas as pd

################################################################################

# --- Setup global variables (available in all functions) ---

# Set the stimuli rotation degree here:
degree = '3'
paradigm = 'control3' # Options: 'main' 
                      #          'control1': Vertical Coloring 
                      #          'control2': Random Coloring
                      #          'control3': Balanced Random Coloring
BG_color = 'grey' # 'grey', 'black'

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))

# Store info about the experiment session
psychopyVersion = '2023.2.3'
expName = 'VDT'  # from the Builder filename that created this script
expInfo = {
    'participant': "sub-",
    'session': f"ses-{paradigm}",
    'run': "run-",
    'date': data.getDateStr(),  # add a simple timestamp
    'expName': expName,
    'psychopyVersion': psychopyVersion,
    'BG_color': BG_color
}

################################################################################

# --- Functions Definition 

def showExpInfoDlg(expInfo):
    # temporarily remove keys which the dialog doesn't need to show
    poppedKeys = {
        'date': expInfo.pop('date', data.getDateStr()),
        'expName': expInfo.pop('expName', expName),
        'psychopyVersion': expInfo.pop('psychopyVersion', psychopyVersion),
    }
    # show participant info dialog
    dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # restore hidden keys
    expInfo.update(poppedKeys)
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = u'data/%s_%s_%s_%s' % (expInfo['participant'], expInfo['session'], expInfo['run'], f"{expName}-{expInfo['date']}")
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath='./VDT_main.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, 
        sortColumns='time'
    )
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    # this outputs to the screen, not a file
    logging.console.setLevel(logging.EXP)
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log', level=logging.EXP)
    
    return logFile


def setupWindow(expInfo=None, win=None):
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=[1512, 982], fullscr=True, screen=1,
            winType='pyglet', allowStencil=False,
            monitor='testMonitor', color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height'
        )
        if expInfo is not None:
            # store frame rate of monitor if we can measure it
            expInfo['frameRate'] = win.getActualFrameRate()
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [-1.0000, -1.0000, -1.0000]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    win.mouseVisible = False
    win.hideMessage()
    return win


def setupInputs(expInfo, thisExp, win):
    # --- Setup input devices ---
    inputs = {}
    ioConfig = {}
    
    # Setup iohub keyboard
    ioConfig['Keyboard'] = dict(use_keymap='psychopy')
    
    ioSession = '1'
    if 'session' in expInfo:
        ioSession = str(expInfo['session'])
    ioServer = io.launchHubServer(window=win, **ioConfig)
    eyetracker = None
    
    # create a default keyboard (e.g. to check for escape)
    defaultKeyboard = keyboard.Keyboard(backend='psychotoolbox')
    # return inputs dict
    return {
        'ioServer': ioServer,
        'defaultKeyboard': defaultKeyboard,
        'eyetracker': eyetracker,
    }

def pauseExperiment(thisExp, inputs=None, win=None, timers=[], playbackComponents=[]):
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # pause any playback components
    for comp in playbackComponents:
        comp.pause()
    # prevent components from auto-drawing
    win.stashAutoDraw()
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # make sure we have a keyboard
        if inputs is None:
            inputs = {
                'defaultKeyboard': keyboard.Keyboard(backend='ioHub')
            }
        # check for quit (typically the Esc key)
        if inputs['defaultKeyboard'].getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win, inputs=inputs)
        # flip the screen
        win.flip()
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, inputs=inputs, win=win)
    # resume any playback components
    for comp in playbackComponents:
        comp.play()
    # restore auto-drawn components
    win.retrieveAutoDraw()
    # reset any timers
    for timer in timers:
        timer.reset()


def run(expInfo, thisExp, win, inputs, globalClock=None, thisSession=None, deg=degree):

    bg_color = expInfo['BG_color']

    # mark experiment as started
    thisExp.status = STARTED
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = inputs['ioServer']
    defaultKeyboard = inputs['defaultKeyboard']
    eyetracker = inputs['eyetracker']
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
        
    # --- Initialize components for Routine "ScannerSync" ---
    trigger = keyboard.Keyboard()
    sync_txt = visual.TextStim(win=win, name='sync_txt',
        text='Scanner Synchronization ...',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0)
    
    # --- Initialize components for Routine "WaitingForSubject" ---
    Vertical = visual.ImageStim(
        win=win,
        name='Vertical', 
        image=f'./images2/circle-{bg_color}.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), size=(2,1),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    key_resp = keyboard.Keyboard()
    
    # --- Initialize components for Routine "VDT" ---
    PresentedLine1 = visual.ImageStim(
        win=win,
        name='PresentedLine1', 
        image=f'./images2/circle-{bg_color}.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), size=(2, 1),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    FixDot2 = visual.ImageStim(
        win=win,
        name='FixDot2', 
        image=f'./images2/circle-{bg_color}.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), size=(2,1),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-1.0)
    key_resp_2 = keyboard.Keyboard()
    
    # create some handy timers
    if globalClock is None:
        globalClock = core.Clock()  # to track the time since experiment started
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6)

    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler(nReps=3.0, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='trials')
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            globals()[paramName] = thisTrial[paramName]
    
    for thisTrial in trials:
        currentLoop = trials
        thisExp.timestampOnFlip(win, 'thisRow.t')
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                inputs=inputs, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
        )
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                globals()[paramName] = thisTrial[paramName]
        
        # --- Prepare to start Routine "ScannerSync" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('ScannerSync.started', globalClock.getTime())
        trigger.keys = []
        trigger.rt = []
        _trigger_allKeys = []
        # keep track of which components have finished
        ScannerSyncComponents = [trigger, sync_txt]
        for thisComponent in ScannerSyncComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "ScannerSync" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *trigger* updates
            waitOnFlip = False
            
            # if trigger is starting this frame...
            if trigger.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                trigger.frameNStart = frameN  # exact frame index
                trigger.tStart = t  # local t and not account for scr refresh
                trigger.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(trigger, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'trigger.started')
                # update status
                trigger.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(trigger.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(trigger.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if trigger.status == STARTED and not waitOnFlip:
                theseKeys = trigger.getKeys(keyList=['t'], ignoreKeys=["escape"], waitRelease=False)
                _trigger_allKeys.extend(theseKeys)
                if len(_trigger_allKeys):
                    trigger.keys = _trigger_allKeys[-1].name  # just the last key pressed
                    trigger.rt = _trigger_allKeys[-1].rt
                    trigger.duration = _trigger_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # *sync_txt* updates
            
            # if sync_txt is starting this frame...
            if sync_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                sync_txt.frameNStart = frameN  # exact frame index
                sync_txt.tStart = t  # local t and not account for scr refresh
                sync_txt.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(sync_txt, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'sync_txt.started')
                # update status
                sync_txt.status = STARTED
                sync_txt.setAutoDraw(True)
            
            # if sync_txt is active this frame...
            if sync_txt.status == STARTED:
                # update params
                pass
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, inputs=inputs, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in ScannerSyncComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "ScannerSync" ---
        for thisComponent in ScannerSyncComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('ScannerSync.stopped', globalClock.getTime())
        # check responses
        if trigger.keys in ['', [], None]:  # No response was made
            trigger.keys = None
        trials.addData('trigger.keys',trigger.keys)
        if trigger.keys != None:  # we had a response
            trials.addData('trigger.rt', trigger.rt)
            trials.addData('trigger.duration', trigger.duration)
        # the Routine "ScannerSync" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
    # completed 3.0 repeats of 'trials'
    
    
    # --- Prepare to start Routine "WaitingForSubject" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('WaitingForScannerTrigger.started', globalClock.getTime())
    key_resp.keys = []
    key_resp.rt = []
    _key_resp_allKeys = []
    # keep track of which components have finished
    WaitingForScannerTriggerComponents = [Vertical, key_resp]
    for thisComponent in WaitingForScannerTriggerComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "WaitingForSubject" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *Vertical* updates
        
        # if Vertical is starting this frame...
        if Vertical.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Vertical.frameNStart = frameN  # exact frame index
            Vertical.tStart = t  # local t and not account for scr refresh
            Vertical.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Vertical, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'Vertical.started')
            # update status
            Vertical.status = STARTED
            Vertical.setAutoDraw(True)
        
        # if Vertical is active this frame...
        if Vertical.status == STARTED:
            # update params
            pass
        
        # *key_resp* updates
        waitOnFlip = False
        
        # if key_resp is starting this frame...
        if key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp.frameNStart = frameN  # exact frame index
            key_resp.tStart = t  # local t and not account for scr refresh
            key_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp.started')
            # update status
            key_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp.status == STARTED and not waitOnFlip:
            theseKeys = key_resp.getKeys(keyList=['s'], ignoreKeys=["escape"], waitRelease=False)
            _key_resp_allKeys.extend(theseKeys)
            if len(_key_resp_allKeys):
                key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                key_resp.rt = _key_resp_allKeys[-1].rt
                key_resp.duration = _key_resp_allKeys[-1].duration
                # was this correct?
                if (key_resp.keys == str("'space'")) or (key_resp.keys == "'space'"):
                    key_resp.corr = 1
                else:
                    key_resp.corr = 0
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, inputs=inputs, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in WaitingForScannerTriggerComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "WaitingForSubject" ---
    for thisComponent in WaitingForScannerTriggerComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('WaitingForScannerTrigger.stopped', globalClock.getTime())
    # check responses
    if key_resp.keys in ['', [], None]:  # No response was made
        key_resp.keys = None
        # was no response the correct answer?!
        if str("'space'").lower() == 'none':
           key_resp.corr = 1;  # correct non-response
        else:
           key_resp.corr = 0;  # failed to respond (incorrectly)
    # store data for thisExp (ExperimentHandler)
    thisExp.addData('key_resp.keys',key_resp.keys)
    thisExp.addData('key_resp.corr', key_resp.corr)
    if key_resp.keys != None:  # we had a response
        thisExp.addData('key_resp.rt', key_resp.rt)
        thisExp.addData('key_resp.duration', key_resp.duration)
    thisExp.nextEntry()
    # the Routine "WaitingForSubject" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    #---------------------------------------------------------------------------
    # Creating proper stimuli order 
    if (paradigm == 'main') | (paradigm=='control1'):
        arr = ['OB', 'OB', 'OB', 'OB', 'ST', 'ST', 'ST', 'ST']
        np.random.shuffle(arr)
        arr2 = ['ST', 'ST'] + arr
        for i in range(len(arr2)):
            if arr2[i] == 'OB':
                arr2[i] = ['OB', 'ST', 'ST']
        arr3 = []
        for i in range(len(arr2)):
            if len(arr2[i]) == 2: 
                arr3 = arr3 + [arr2[i]]
            else: 
                arr3 = arr3 + arr2[i]
        for i in range(len(arr3)):
            if arr3[i] == 'ST':
                arr3[i] = 1
            else:
                arr3[i] = 0        
        idx = np.where(arr3)[0]
        np.random.shuffle(idx)
        idxx = list(idx[0:7])
        for i in idxx:
            arr3[i] = 2

    elif paradigm == 'control2':
        arr = ['OB', 'OB', 'OB', 'OB', 'ST', 'ST', 'ST', 'ST']
        np.random.shuffle(arr)
        arr2 = ['ST', 'ST'] + arr
        for i in range(len(arr2)):
            if arr2[i] == 'OB':
                arr2[i] = ['OB', 'ST', 'ST']
        arr3 = []
        for i in range(len(arr2)):
            if len(arr2[i]) == 2: 
                arr3 = arr3 + [arr2[i]]
            else: 
                arr3 = arr3 + arr2[i]
        for i in range(len(arr3)):
            if arr3[i] == 'ST':
                arr3[i] = 1
            else:
                arr3[i] = 0        
        idx = np.where(arr3)[0]
        np.random.shuffle(idx)
        idxx = list(idx[0:7])
        for i in idxx:
            arr3[i] = 2

        arr_c = ['Y', 'Y', 'Y', 'Y', 'W', 'W', 'W', 'W']
        np.random.shuffle(arr_c)
        arr2_c = ['W', 'W'] + arr_c
        for i in range(len(arr2_c)):
            if arr2_c[i] == 'Y':
                arr2_c[i] = ['Y', 'W', 'W']
        arr3_c = []
        for i in range(len(arr2_c)):
            if len(arr2_c[i]) == 1: 
                arr3_c = arr3_c + [arr2_c[i]]
            else: 
                arr3_c = arr3_c + arr2_c[i]
        for i in range(len(arr3_c)):
            if arr3_c[i] == 'W':
                arr3_c[i] = 1
            else:
                arr3_c[i] = 0 

    elif paradigm == 'control3':
        arr = ['OB', 'OB', 'OB', 'OB', 'ST', 'ST', 'ST', 'ST']
        np.random.shuffle(arr)
        arr2 = ['ST', 'ST'] + arr
        for i in range(len(arr2)):
            if arr2[i] == 'OB':
                arr2[i] = ['OB', 'ST', 'ST']
        arr3 = []
        for i in range(len(arr2)):
            if len(arr2[i]) == 2: 
                arr3 = arr3 + [arr2[i]]
            else: 
                arr3 = arr3 + arr2[i]
        for i in range(len(arr3)):
            if arr3[i] == 'ST':
                arr3[i] = 1
            else:
                arr3[i] = 0        
        idx = np.where(arr3)[0]
        np.random.shuffle(idx)
        idxx = list(idx[0:7])
        for i in idxx:
            arr3[i] = 2
        idx0 = np.where(np.array(arr3)==0)[0]
        idx1 = np.where(np.array(arr3)==1)[0]
        idx2 = np.where(np.array(arr3)==2)[0]

        np.random.shuffle(idx0)
        np.random.shuffle(idx1)
        np.random.shuffle(idx2)

        arr3_cc = arr3
        arr3_cc[idx0[0]] = 'OBY'
        arr3_cc[idx0[1]] = 'OBY'
        arr3_cc[idx0[2]] = 'STCY'
        arr3_cc[idx0[3]] = 'STCCY'      

        for i in range(6):
            arr3_cc[idx1[i]]='STCW'
            arr3_cc[idx2[i]]='STCCW'
    
        idx_obw = np.where([isinstance(i, int) for i in arr3_cc])[0]
        for i in range(2):
            arr3_cc[idx_obw[i]] = 'OBW'    

    df = pd.DataFrame([])
    
    if paradigm == 'main':
        df['image'] = [f'./images2/Sphere_Ref_BG-{bg_color}_stim-white.png']*len(arr3)
        for i in range(len(df)):
            if arr3[i] == 1:
                df.loc[i, 'image'] = f'./images2/Sphere_CW-{deg}_BG-{bg_color}_stim-white.png'
            elif arr3[i] == 2:
                df.loc[i, 'image'] = f'./images2/Sphere_CCW-{deg}_BG-{bg_color}_stim-white.png'

    elif paradigm == 'control1':
        df['image'] = [f'./images2/Sphere_Ref_BG-{bg_color}_stim-yellow.png']*len(arr3)
        for i in range(len(df)):
            if arr3[i] == 1:
                df.loc[i, 'image'] = f'./images2/Sphere_CW-{deg}_BG-{bg_color}_stim-white.png'
            elif arr3[i] == 2:
                df.loc[i, 'image'] = f'./images2/Sphere_CCW-{deg}_BG-{bg_color}_stim-white.png'

    elif paradigm == 'control2':
        df['image'] = [f'./images2/Sphere_Ref_BG-{bg_color}_stim-white.png']*len(arr3)
        for i in range(len(df)):
            if arr3[i] == 1:
                if arr3_c[i]:
                    df.loc[i, 'image'] = f'./images2/Sphere_CW-{deg}_BG-{bg_color}_stim-white.png'
                else:
                    df.loc[i, 'image'] = f'./images2/Sphere_CW-{deg}_BG-{bg_color}_stim-yellow.png'
            elif arr3[i] == 2:
                if arr3_c[i]:
                    df.loc[i, 'image'] = f'./images2/Sphere_CCW-{deg}_BG-{bg_color}_stim-white.png'
                else:
                    df.loc[i, 'image'] = f'./images2/Sphere_CCW-{deg}_BG-{bg_color}_stim-yellow.png'
            elif arr3[i] == 0:
                if arr3_c[i]:
                    df.loc[i, 'image'] = f'./images2/Sphere_Ref_BG-{bg_color}_stim-white.png'
                else:
                    df.loc[i, 'image'] = f'./images2/Sphere_Ref_BG-{bg_color}_stim-yellow.png'

    elif paradigm == 'control3':
        df['image'] = [f'./images2/Sphere_Ref_BG-{bg_color}_stim-white.png']*len(arr3)
        for i in range(len(df)):
            if arr3_cc[i] == 'OBW':
                df.loc[i, 'image'] = f'./images2/Sphere_Ref_BG-{bg_color}_stim-white.png'
            elif arr3_cc[i] == 'OBY':
                df.loc[i, 'image'] = f'./images2/Sphere_Ref_BG-{bg_color}_stim-yellow.png'
            elif arr3_cc[i] == 'STCW':
                df.loc[i, 'image'] = f'./images2/Sphere_CW-{deg}_BG-{bg_color}_stim-white.png'
            elif arr3_cc[i] == 'STCY':
                df.loc[i, 'image'] = f'./images2/Sphere_CW-{deg}_BG-{bg_color}_stim-yellow.png'
            elif arr3_cc[i] == 'STCCW':
                df.loc[i, 'image'] = f'./images2/Sphere_CCW-{deg}_BG-{bg_color}_stim-white.png'
            elif arr3_cc[i] == 'STCCY':
                df.loc[i, 'image'] = f'./images2/Sphere_CCW-{deg}_BG-{bg_color}_stim-yellow.png'


    df.to_excel('./loopTemplate18.xlsx', index=False)
    #---------------------------------------------------------------------------
    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler(nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions('loopTemplate18.xlsx'),
        seed=None, name='trials')
    
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            globals()[paramName] = thisTrial[paramName]
        
    for thisTrial in trials:
        print(thisTrial)
        currentLoop = trials
        thisExp.timestampOnFlip(win, 'thisRow.t')
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                inputs=inputs, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
        )
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                globals()[paramName] = thisTrial[paramName]
        
        # --- Prepare to start Routine "VDT" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('VDT.started', globalClock.getTime())
        PresentedLine1.setImage(image)
        key_resp_2.keys = []
        key_resp_2.rt = []
        _key_resp_2_allKeys = []
        # keep track of which components have finished
        VDTComponents = [PresentedLine1, FixDot2, key_resp_2]
        for thisComponent in VDTComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "VDT" ---
        routineForceEnded = not continueRoutine
        jitter = 0.1 #seconds 
        while continueRoutine and routineTimer.getTime() < 1.0 + (random()-0.5)/(1/(2*jitter)): # With Jitter
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *PresentedLine1* updates
            
            # if PresentedLine1 is starting this frame...
            if PresentedLine1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                PresentedLine1.frameNStart = frameN  # exact frame index
                PresentedLine1.tStart = t  # local t and not account for scr refresh
                PresentedLine1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(PresentedLine1, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'PresentedLine1.started')
                # update status
                PresentedLine1.status = STARTED
                PresentedLine1.setAutoDraw(True)
            
            # if PresentedLine1 is active this frame...
            if PresentedLine1.status == STARTED:
                # update params
                pass
            
            # if PresentedLine1 is stopping this frame...
            if PresentedLine1.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > PresentedLine1.tStartRefresh + .75-frameTolerance:
                    # keep track of stop time/frame for later
                    PresentedLine1.tStop = t  # not accounting for scr refresh
                    PresentedLine1.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'PresentedLine1.stopped')
                    # update status
                    PresentedLine1.status = FINISHED
                    PresentedLine1.setAutoDraw(False)
            
            # *FixDot2* updates
            
            # if FixDot2 is starting this frame...
            if FixDot2.status == NOT_STARTED and tThisFlip >= .75-frameTolerance:
                # keep track of start time/frame for later
                FixDot2.frameNStart = frameN  # exact frame index
                FixDot2.tStart = t  # local t and not account for scr refresh
                FixDot2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(FixDot2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'FixDot2.started')
                # update status
                FixDot2.status = STARTED
                FixDot2.setAutoDraw(True)
            
            # if FixDot2 is active this frame...
            if FixDot2.status == STARTED:
                # update params
                pass
            
            # if FixDot2 is stopping this frame...
            if FixDot2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > FixDot2.tStartRefresh + .25-frameTolerance:
                    # keep track of stop time/frame for later
                    FixDot2.tStop = t  # not accounting for scr refresh
                    FixDot2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'FixDot2.stopped')
                    # update status
                    FixDot2.status = FINISHED
                    FixDot2.setAutoDraw(False)
            
            # *key_resp_2* updates
            waitOnFlip = False
            
            # if key_resp_2 is starting this frame...
            if key_resp_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                key_resp_2.frameNStart = frameN  # exact frame index
                key_resp_2.tStart = t  # local t and not account for scr refresh
                key_resp_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp_2.started')
                # update status
                key_resp_2.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
            
            # if key_resp_2 is stopping this frame...
            if key_resp_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > key_resp_2.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    key_resp_2.tStop = t  # not accounting for scr refresh
                    key_resp_2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'key_resp_2.stopped')
                    # update status
                    key_resp_2.status = FINISHED
                    key_resp_2.status = FINISHED
            if key_resp_2.status == STARTED and not waitOnFlip:
                theseKeys = key_resp_2.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
                _key_resp_2_allKeys.extend(theseKeys)
                if len(_key_resp_2_allKeys):
                    key_resp_2.keys = [key.name for key in _key_resp_2_allKeys]  # storing all keys
                    key_resp_2.rt = [key.rt for key in _key_resp_2_allKeys]
                    key_resp_2.duration = [key.duration for key in _key_resp_2_allKeys]
                    # was this correct?
                    if (key_resp_2.keys == str("'space'")) or (key_resp_2.keys == "'space'"):
                        key_resp_2.corr = 1
                    else:
                        key_resp_2.corr = 0
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, inputs=inputs, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in VDTComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "VDT" ---
        for thisComponent in VDTComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('VDT.stopped', globalClock.getTime())
        # check responses
        if key_resp_2.keys in ['', [], None]:  # No response was made
            key_resp_2.keys = None
            # was no response the correct answer?!
            if str("'space'").lower() == 'none':
               key_resp_2.corr = 1;  # correct non-response
            else:
               key_resp_2.corr = 0;  # failed to respond (incorrectly)
        # store data for trials (TrialHandler)
        trials.addData('key_resp_2.keys',key_resp_2.keys)
        trials.addData('key_resp_2.corr', key_resp_2.corr)
        if key_resp_2.keys != None:  # we had a response
            trials.addData('key_resp_2.rt', key_resp_2.rt[0])
            trials.addData('key_resp_2.duration', key_resp_2.duration[0])
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.000000)
        thisExp.nextEntry()
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
    # completed 2.0 repeats of 'trials'
    
    
    # mark experiment as finished
    endExperiment(thisExp, win=win, inputs=inputs)


def saveData(thisExp):
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, inputs=None, win=None):
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # mark experiment handler as finished
    thisExp.status = FINISHED
    # shut down eyetracker, if there is one
    if inputs is not None:
        if 'eyetracker' in inputs and inputs['eyetracker'] is not None:
            inputs['eyetracker'].setConnectionState(False)
    logging.flush()


def quit(thisExp, win=None, inputs=None, thisSession=None):
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    if inputs is not None:
        if 'eyetracker' in inputs and inputs['eyetracker'] is not None:
            inputs['eyetracker'].setConnectionState(False)
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
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