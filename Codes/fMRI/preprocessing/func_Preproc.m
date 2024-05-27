function func_Preproc(ffiles, sfile, save_path, subj_name, TR, echo_time, total_EPI_rot)

%% Run Preprocessing Batch
spm fmri;
matlabbatch = func_PreprocBatch(ffiles, sfile, echo_time, total_EPI_rot);
spm_jobman('run', matlabbatch)

%% Deleting unnecessary files and moving results to the related folder
 
% Functional data
motionCorrectedDir = fullfile(save_path, subj_name, ...
    'func', 'restMotionCorrected');
mkdir(motionCorrectedDir);
tmp = split(ffiles{1}(1,:), '/');
fdir = join(tmp(1:end-1), '/');
datapath = fdir{1};
delete([datapath '/ra*.*']);
delete([datapath '/meanra*.*']);
delete([datapath '/smeanrau*.*']);
delete([datapath '/*.mat']);
delete([datapath '/u*.*'])
movefile([datapath '/swrau*.*'], motionCorrectedDir);
movefile([datapath '/rp_*.txt'], motionCorrectedDir);
movefile([datapath '/wrau*.*'], motionCorrectedDir);
 
% GRE-Field Data
peresDir = fullfile(save_path, subj_name, 'fmap');
mkdir(peresDir);
tmp = split(ffiles{3}(1,:), '/');
fdir = join(tmp(1:end-1), '/');
datapath = fdir{1};
delete([datapath '/fpm*.*']);
delete([datapath '/sc*.*']);
movefile([datapath '/vdm*.*'], peresDir);
 
% Structural Data
stresDir = fullfile(save_path, subj_name, 'anat');
mkdir(stresDir);
tmp = split(sfile(1:end), '/');
sdir = join(tmp(1:end-1), '/');
datapath = sdir{1};
delete([datapath '/cat*.mat']);
delete([datapath '/cat*.jpg']);
delete([datapath '/cat*.txt']);
delete([datapath '/cat*.xml']);
delete([datapath '/msub*.*']);
movefile([datapath '/mwp1*.*'], stresDir);
movefile([datapath '/mwp2*.*'], stresDir);
movefile([datapath '/mwp3*.*'], stresDir);
movefile([datapath '/wmsub*.*'], stresDir);
movefile([datapath '/y_*.*'], stresDir);
movefile([datapath '/iy_*.*'], stresDir);
movefile([datapath '/cat*.pdf'], stresDir);
 
%% Run Artifact Detection Batch
  
clear matlabbatch;
[matlabbatch, art_pth] = func_ArtDetection_batch(motionCorrectedDir, save_path, subj_name, TR);
spm_jobman('serial', matlabbatch);
art_batch(fullfile(art_pth, 'SPM.mat'));