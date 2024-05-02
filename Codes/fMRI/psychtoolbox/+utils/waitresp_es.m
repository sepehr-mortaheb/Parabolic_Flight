% Written by Frederic Peters 1/4/2015 
% Editted by Sepehr Mortaheb 17/2/2022 
% Wait for a single key to be pressed and released 
%(version Psychtoolbox 3.0.18 2021)
% 
% Usage:
% [pressid,timeSecs, pressti]=waitresp(trmax, type, os)
%
% Where (trmax) is the maximum amount of time allowed (in seconds) for 
% pressing a key, (type) determines whether the program is running on a 
% computer/laptop ("comp") or on the scanner system ("scanner"), and (os)
% determines the operating system that the codes are running on with the 
% options of OS-MAC ("mac") or Windows ("win"). 
% This function will return three variables: (i) pressid (key pressed id)
% (ii) timeSecs (the time of key press) and (iii) pressti (key press reaction time);   
% An additional parameter can be set up, restricting allowed keys. By 
% default, the command lines for RestrictKeysForKbCheck usage are 
% commented. Some MRI users (e.g. Prisma) may want to restrict allowed
% keys, as the scanner will trigger a character code at the beginning of each TR 
% period (e.g. the letter "t", code 84).  
 
function [pressid, timeSecs, pressti]=waitresp_es(trmax, sys_type)

switch sys_type 
    case 'mac'
        RestrictKeysForKbCheck([41,...
                                KbName('d'), KbName('f'), ...
                                KbName('h'), KbName('j')]); %QWERTY keyboard
    case 'scanner'
        RestrictKeysForKbCheck([27,...
                                KbName('b'), KbName('y'), ...
                                KbName('g'), KbName('r')]); % 2-button response box 
end
                                          
while KbCheck; end

pressid=[];
pressti=[];

startSecs = GetSecs; % Checking time

while isempty(pressid) && GetSecs < startSecs+trmax
    [keyIsDown, timeSecs, keyCode] = KbCheck;
    if keyIsDown > 0
        pressid = find(keyCode);
        pressti = timeSecs - startSecs;
        while KbCheck; end         
        if pressid
            break;
        end
    end
end
if isempty(pressid)==1
    pressid = 99; %% If no key is pressed, this function will return #99 as pressid value
end
