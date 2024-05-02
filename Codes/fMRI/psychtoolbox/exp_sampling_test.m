clc;
clear; 
sca; 
close; 

%% Initialization 
subj = 'test';
sys_type = 'mac';

addpath('./necessary_files');
addpath('./log_files');

fid = fopen(fullfile(pwd, 'log_files', [subj '_ExpSamp_test_log.txt']), 'w');

%% Setting up the Psychtoolbox

PTB_struct = utils.PTB_config(sys_type);

%% Experience Sampling Settings 
ES_struct = struct;
ES_struct.N_trials = 3; 
ES_struct.min_dur = 3; 
ES_struct.max_dur = 5; 

%% Introduction
Lines = ['Try to stay awake and let your mind wander.' ... 
         '\n\n A beep will notify you to report on the state of your mind.' ... 
         '\n\n Answer by pressing one of the buttons as will be shown in the picture.' ... 
         '\n\n Whenever you are ready, press any button to start the task.'];

% Introduction Page 
DrawFormattedText(PTB_struct.window, Lines, ...
                      'center', PTB_struct.pixelsY*0.25, PTB_struct.white);
Screen('Flip', PTB_struct.window);
utils.waitresp(inf, sys_type);

%% Task 

fprintf(fid, 'Start of ES Task Function at %f\n\n', GetSecs);
tasks.Experience_Sampling(ES_struct, PTB_struct, fid, sys_type); 
fprintf(fid, '\n');

%% Termination 
RestrictKeysForKbCheck([]);
fclose(fid);
sca;
