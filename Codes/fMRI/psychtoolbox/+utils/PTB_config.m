function PTB_struct = PTB_config(sys_type)

% Window Settings
PTB_struct = struct; 
if strcmp(sys_type, 'mac')
    Screen('Preference', 'SkipSyncTests', 1)                                % Skip synchronization test
end
PsychDefaultSetup(2);                                                       % Some default setting for setting up Psychtoolbox
PTB_struct.screens = Screen('Screens');                                     % Get Screen numbers
if strcmp(sys_type, 'scanner')
    PTB_struct.screenNum = 1;                                               % Choosing the external display if exists 
else
    PTB_struct.screenNum = max(PTB_struct.screens);
end
PTB_struct.black = BlackIndex(PTB_struct.screenNum);                        % Define Black which is 0
PTB_struct.white = WhiteIndex(PTB_struct.screenNum);                        % Define White which is 1 Opening an on-screen window 
                                                                            % and color it black:
[PTB_struct.window, PTB_struct.windowRect] = PsychImaging('OpenWindow', ...
    PTB_struct.screenNum, PTB_struct.black);
[PTB_struct.pixelsX, PTB_struct.pixelsY] = Screen('windowSize', ...
    PTB_struct.window);                                                     % Size of the window in pixels
[PTB_struct.centerX, PTB_struct.centerY] = ...
    RectCenter(PTB_struct.windowRect);                                      % Center of the window coordinates in pixels
Screen('TextSize', PTB_struct.window, 30);                                  % Size of the text 
Screen('TextFont', PTB_struct.window, 'Arial');                             % Font of the Text 
MaxPriority(PTB_struct.window);                                             % Giving top priroty to the program in the processor 
