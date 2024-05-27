function func_Preproc(ffiles, sfile, save_path, subj_name, TR)

%% Run Preprocessing Batch
spm fmri;
matlabbatch = func_PreprocBatch(ffiles, sfile);
spm_jobman('run', matlabbatch)

%% Deleting unnecessary files and moving results to the related folder
% 
% % Functional data
% motionCorrectedDir = fullfile(save_path, subj_name, ...
%     'func', 'restMotionCorrected');
% mkdir(motionCorrectedDir);
% tmp = split(ffiles{1}(1,:), '/');
% fdir = join(tmp(1:end-1), '/');
% datapath = fdir{1};
% delete([datapath '/ra*.*']);
% delete([datapath '/meanra*.*']);
% delete([datapath '/smeanrau*.*']);
% delete([datapath '/*.mat']);
% delete([datapath '/u*.*'])
% movefile([datapath '/srau*.*'], motionCorrectedDir);
% movefile([datapath '/rp_*.txt'], motionCorrectedDir);
%  
% % GRE-Field Data
% peresDir = fullfile(save_path, subj_name, 'fmap');
% mkdir(peresDir);
% tmp = split(ffiles{3}(1,:), '/');
% fdir = join(tmp(1:end-1), '/');
% datapath = fdir{1};
% delete([datapath '/fpm*.*']);
% delete([datapath '/sc*.*']);
% movefile([datapath '/vdm*.*'], peresDir);
% 
% % Structural Data
% stresDir = fullfile(save_path, subj_name, 'anat');
% mkdir(stresDir);
% tmp = split(sfile(1:end), '/');
% sdir = join(tmp(1:end-1), '/');
% datapath = sdir{1};
% delete([datapath '/cat*.mat']);
% delete([datapath '/cat*.jpg']);
% delete([datapath '/cat*.txt']);
% delete([datapath '/cat*.xml']);
% delete([datapath '/y_*.*']);
% movefile([datapath '/p1*.*'], stresDir);
% movefile([datapath '/p2*.*'], stresDir);
% movefile([datapath '/p3*.*'], stresDir);
% movefile([datapath '/cat*.pdf'], stresDir);
% 
% %% Run Artifact Detection Batch
%  
% clear matlabbatch;
% 
% matlabbatch = func_pipeline.func_artdetection_batch(motionCorrectedDir, save_path, subj_name, TR);
% spm_jobman('serial', matlabbatch);
% art_batch(fullfile(art_pth, 'SPM.mat'));