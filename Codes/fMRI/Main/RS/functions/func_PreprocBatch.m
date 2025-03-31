function matlabbatch = func_PreprocBatch(inpfiles, AcqParams, Dirs)

spm_dir = Dirs.spm;
fdata = inpfiles{1};
meanfdata = inpfiles{2};
sdata = inpfiles{3};

tr = AcqParams.tr;

%% Reading the structural and functional data 
matlabbatch{1}.cfg_basicio.file_dir.file_ops.cfg_named_file.name = 'struct';
matlabbatch{1}.cfg_basicio.file_dir.file_ops.cfg_named_file.files = {{sdata}};
matlabbatch{2}.cfg_basicio.file_dir.file_ops.cfg_named_file.name = 'func';
matlabbatch{2}.cfg_basicio.file_dir.file_ops.cfg_named_file.files = {{fdata}};
matlabbatch{3}.cfg_basicio.file_dir.file_ops.cfg_named_file.name = 'func_mean';
matlabbatch{3}.cfg_basicio.file_dir.file_ops.cfg_named_file.files = {{meanfdata}};

%% Segmentation and Normalization using CAT12
matlabbatch{4}.spm.tools.cat.estwrite.data(1) = cfg_dep('Named File Selector: struct(1) - Files', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files', '{}',{1}));
matlabbatch{4}.spm.tools.cat.estwrite.data_wmh = {''};
matlabbatch{4}.spm.tools.cat.estwrite.nproc = 4;
matlabbatch{4}.spm.tools.cat.estwrite.useprior = '';
matlabbatch{4}.spm.tools.cat.estwrite.opts.tpm = {fullfile(spm_dir, 'tpm', 'TPM.nii')};
matlabbatch{4}.spm.tools.cat.estwrite.opts.affreg = 'mni';
matlabbatch{4}.spm.tools.cat.estwrite.opts.biasacc = 0.5;
matlabbatch{4}.spm.tools.cat.estwrite.extopts.restypes.optimal = [1 0.3];
matlabbatch{4}.spm.tools.cat.estwrite.extopts.setCOM = 1;
matlabbatch{4}.spm.tools.cat.estwrite.extopts.APP = 1070;
matlabbatch{4}.spm.tools.cat.estwrite.extopts.affmod = 0;
matlabbatch{4}.spm.tools.cat.estwrite.extopts.spm_kamap = 0;
matlabbatch{4}.spm.tools.cat.estwrite.extopts.LASstr = 0.5;
matlabbatch{4}.spm.tools.cat.estwrite.extopts.LASmyostr = 0;
matlabbatch{4}.spm.tools.cat.estwrite.extopts.gcutstr = 2;
matlabbatch{4}.spm.tools.cat.estwrite.extopts.WMHC = 2;
matlabbatch{4}.spm.tools.cat.estwrite.extopts.registration.shooting.shootingtpm = {fullfile(spm_dir, 'toolbox', 'cat12', 'templates_MNI152NLin2009cAsym', 'Template_0_GS.nii')};
matlabbatch{4}.spm.tools.cat.estwrite.extopts.registration.shooting.regstr = 0.5;
matlabbatch{4}.spm.tools.cat.estwrite.extopts.vox = 1.5;
matlabbatch{4}.spm.tools.cat.estwrite.extopts.bb = 12;
matlabbatch{4}.spm.tools.cat.estwrite.extopts.SRP = 22;
matlabbatch{4}.spm.tools.cat.estwrite.extopts.ignoreErrors = 1;
matlabbatch{4}.spm.tools.cat.estwrite.output.BIDS.BIDSno = 1;
matlabbatch{4}.spm.tools.cat.estwrite.output.surface = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.surf_measures = 1;
matlabbatch{4}.spm.tools.cat.estwrite.output.ROImenu.noROI = struct([]);
matlabbatch{4}.spm.tools.cat.estwrite.output.GM.native = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.GM.mod = 1;
matlabbatch{4}.spm.tools.cat.estwrite.output.GM.dartel = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.WM.native = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.WM.mod = 1;
matlabbatch{4}.spm.tools.cat.estwrite.output.WM.dartel = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.CSF.native = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.CSF.warped = 1;
matlabbatch{4}.spm.tools.cat.estwrite.output.CSF.mod = 1;
matlabbatch{4}.spm.tools.cat.estwrite.output.CSF.dartel = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.ct.native = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.ct.warped = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.ct.dartel = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.pp.native = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.pp.warped = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.pp.dartel = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.WMH.native = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.WMH.warped = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.WMH.mod = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.WMH.dartel = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.SL.native = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.SL.warped = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.SL.mod = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.SL.dartel = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.TPMC.native = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.TPMC.warped = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.TPMC.mod = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.TPMC.dartel = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.atlas.native = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.label.native = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.label.warped = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.label.dartel = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.labelnative = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.bias.warped = 1;
matlabbatch{4}.spm.tools.cat.estwrite.output.las.native = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.las.warped = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.las.dartel = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.jacobianwarped = 0;
matlabbatch{4}.spm.tools.cat.estwrite.output.warps = [1 1];
matlabbatch{4}.spm.tools.cat.estwrite.output.rmat = 0;

%% Coregistration of Functional Data to the T1 Space
matlabbatch{5}.spm.spatial.coreg.estimate.ref(1) = cfg_dep('Named File Selector: struct(1) - Files', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files', '{}',{1}));
matlabbatch{5}.spm.spatial.coreg.estimate.source(1) = cfg_dep('Named File Selector: func_mean(1) - Files', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files', '{}',{1}));
matlabbatch{5}.spm.spatial.coreg.estimate.other(1) = cfg_dep('Named File Selector: func(1) - Files', substruct('.','val', '{}',{2}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files', '{}',{1}));
matlabbatch{5}.spm.spatial.coreg.estimate.eoptions.cost_fun = 'nmi';
matlabbatch{5}.spm.spatial.coreg.estimate.eoptions.sep = [4 2];
matlabbatch{5}.spm.spatial.coreg.estimate.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
matlabbatch{5}.spm.spatial.coreg.estimate.eoptions.fwhm = [7 7];

%% Normalization of Functional Data to the MNI Space 
matlabbatch{6}.spm.spatial.normalise.write.subj.def(1) = cfg_dep('CAT12: Segmentation: Deformation Field', substruct('.','val', '{}',{4}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('()',{1}, '.','fordef', '()',{':'}));
matlabbatch{6}.spm.spatial.normalise.write.subj.resample(1) = cfg_dep('Coregister: Estimate: Coregistered Images', substruct('.','val', '{}',{5}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','cfiles'));
matlabbatch{6}.spm.spatial.normalise.write.woptions.bb = [-Inf -Inf -Inf
                                                          Inf Inf Inf];
matlabbatch{6}.spm.spatial.normalise.write.woptions.vox = [2 2 2];
matlabbatch{6}.spm.spatial.normalise.write.woptions.interp = 4;
matlabbatch{6}.spm.spatial.normalise.write.woptions.prefix = 'w';

%% Smoothing
matlabbatch{7}.spm.spatial.smooth.data(1) = cfg_dep('Normalise: Write: Normalised Images (Subj 1)', substruct('.','val', '{}',{6}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('()',{1}, '.','files'));
matlabbatch{7}.spm.spatial.smooth.fwhm = [6 6 6];
matlabbatch{7}.spm.spatial.smooth.dtype = 0;
matlabbatch{7}.spm.spatial.smooth.im = 0;
matlabbatch{7}.spm.spatial.smooth.prefix = 's';
