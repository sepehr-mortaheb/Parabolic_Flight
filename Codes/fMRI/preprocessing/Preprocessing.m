clc 
clear 

%% Initialization 

% --- Set the following directories --- 

% Directory of the BIDS formated data:
bids_dir = '/Users/sepehrmortaheb/MyDrive/LEIA/Projects/Parabolic-Flight/Data/fMRI/LEIA/raw_BIDS';
% Save directory of the fMRI processing:
out_dir_func = '/Users/sepehrmortaheb/MyDrive/LEIA/Projects/Parabolic-Flight/Results/fMRI/LEIA/preprocessed';
% ART directory:
art_dir = which('art');
art_dir(end-4:end) = [];
% SPM directory: 
spm_dir = which('spm');
spm_dir(end-4:end) = [];

% --- Set the following variables --- 

% Subject list [Ex: {'sub-STDXXX'; 'sub-OPTXXX'}]
subj_list = {'sub-SJ'};

% Repetition Time (RT) of the functional acquisition (seconds)
func_TR = 1; 
% Echo time of (TE) of the functional data (ms)
echo_time = [4.92 7.38];
% Total EPI read-out time (ms)
total_EPI_rot = 46.48;

% --- adding other directories ---

addpath(art_dir);
addpath(spm_dir);
addpath(fullfile(spm_dir, 'src'));

%% Functional Pipeline 

for subj_num = 1:numel(subj_list)
    subj = subj_list{subj_num};
    func_PipelineSS(bids_dir, out_dir_func, subj, func_TR, echo_time, total_EPI_rot);
end