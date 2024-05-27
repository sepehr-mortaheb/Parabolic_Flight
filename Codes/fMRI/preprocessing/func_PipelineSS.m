function func_PipelineSS(data_dir, out_dir, subj, TR, echo_time, total_EPI_rot)

%% Initialization
if ~isfolder(out_dir)
    mkdir(out_dir);
end

%% Reading the data
subj_dir = fullfile(data_dir, subj);
ffiles = func_ReadFiles(subj_dir);
sfile = fullfile(data_dir, subj, 'anat', [subj '_T1w.nii']);

%% Preprocessing
func_Preproc(ffiles, sfile, out_dir, subj, TR, echo_time, total_EPI_rot)
close all
