function Experience_Sampling(ES_struct, PTB_struct, fid, sys_type)

MaxPriority(PTB_struct.window); 

N_trials = ES_struct.N_trials; 
min_dur = ES_struct.min_dur;
max_dur = ES_struct.max_dur;

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

Q1_dir = './necessary_files/images_II/Q1_ES.png'; % Question directory
Q1_img = imread(Q1_dir); % Question image 
Q1_image = Screen('MakeTexture', PTB_struct.window, Q1_img); % Question texture

Q2_Past_dir = './necessary_files/images_II/Q2_ES_Past.png';
Q2_Past_img = imread(Q2_Past_dir); 
Q2_Past_image = Screen('MakeTexture', PTB_struct.window, Q2_Past_img);

Q2_Present_dir = './necessary_files/images_II/Q2_ES_Present.png';
Q2_Present_img = imread(Q2_Present_dir); 
Q2_Present_image = Screen('MakeTexture', PTB_struct.window, Q2_Present_img);

Q2_Future_dir = './necessary_files/images_II/Q2_ES_Future.png';
Q2_Future_img = imread(Q2_Future_dir); 
Q2_Future_image = Screen('MakeTexture', PTB_struct.window, Q2_Future_img);

% Trials  
rest_durs = min_dur + (max_dur - min_dur)*rand(1, N_trials);

%% Synching with the Scanner 

DrawFormattedText(PTB_struct.window, 'The experiment will begin in some seconds!',...
        'center', PTB_struct.pixelsY*0.25, PTB_struct.white);
Screen('Flip', PTB_struct.window); 

count = 0; 
while count < 6
    KbTriggerWait(KbName('t')); 
    while KbCheck; end 
    fprintf(fid, 'Trigger %d at %f\n\n', count+1, GetSecs);
    count = count + 1; 
end 

DrawFormattedText(PTB_struct.window, 'Ready?', ...
                      'center', PTB_struct.pixelsY*0.25, PTB_struct.white);
Screen('Flip', PTB_struct.window);
WaitSecs(2); 
DrawFormattedText(PTB_struct.window, 'Go ... ', ...
                      'center', PTB_struct.pixelsY*0.25, PTB_struct.white);
Screen('Flip', PTB_struct.window);
WaitSecs(1); 

%% Task code 

% Start of the task 
t_start = GetSecs; 
fprintf(fid, 'Start at %f\n\n', t_start);

for trial=1:N_trials
    % Showing cross sign for the rest period 
    DrawFormattedText(PTB_struct.window, '+', 'center', 'center', PTB_struct.white);
    Screen('Flip', PTB_struct.window);
    fprintf(fid, 'Start of Trial Number %d at %f\n\n', trial, GetSecs);
    probe_time = WaitSecs(rest_durs(trial)); 
    
    % Showing exclamation mark for probe 
    fprintf(fid, 'Start of Probe at %f\n\n', probe_time);
    DrawFormattedText(PTB_struct.window, '!', 'center', 'center', PTB_struct.white);
    Screen('Flip', PTB_struct.window);
    Q_time = WaitSecs(1);
    
    % Shwoing the question 
    fprintf(fid, 'Start of Question at %f\n\n', Q_time);
    Screen('DrawTexture', PTB_struct.window, Q1_image, [], [], 0); 
    Screen('Flip', PTB_struct.window);
    
    % Waiting for the answer 
    [ans1, secs, ~] = utils.waitresp_es(10, sys_type);
    ans1 = KbName(ans1);
    fprintf(fid, 'Answer to the Question was %s at %f\n\n', ans1, secs);
    
    if ans1=='g' || ans1=='h' % past 
        Screen('DrawTexture', PTB_struct.window, Q2_Past_image, [], [], 0); 
        Screen('Flip', PTB_struct.window);
        [ans2, secs, ~] = utils.waitresp_es(10, sys_type);
        ans2 = KbName(ans2);
        fprintf(fid, 'Answer to Question 2 was %s at %f\n\n', ans2, secs);
    elseif ans1=='y' || ans1=='f' % Present
        Screen('DrawTexture', PTB_struct.window, Q2_Present_image, [], [], 0); 
        Screen('Flip', PTB_struct.window);
        [ans2, secs, ~] = utils.waitresp_es(10, sys_type);
        ans2 = KbName(ans2);
        fprintf(fid, 'Answer to Question 2 was %s at %f\n\n', ans2, secs);
    elseif ans1=='b' || ans1=='d' % Future
        Screen('DrawTexture', PTB_struct.window, Q2_Future_image, [], [], 0); 
        Screen('Flip', PTB_struct.window);
        [ans2, secs, ~] = utils.waitresp_es(10, sys_type);
        ans2 = KbName(ans2);
        fprintf(fid, 'Answer to Question 2 was %s at %f\n\n', ans2, secs); 
    end
end

% Finishing codes 
t_finish = GetSecs; 
fprintf(fid, 'Finish of ExpSamp task at %f\n\n', t_finish);

DrawFormattedText(PTB_struct.window, 'Finish!', ...
                      'center', PTB_struct.pixelsY*0.25, PTB_struct.white);
Screen('Flip', PTB_struct.window);
utils.waitresp(inf, sys_type);

