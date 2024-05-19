%The following code is adapted from Dr. Jeanette Mumford's code by Benedetta Cecconi 
%You can find her code at this link: https://www.dropbox.com/sh/zp4foawa4c5w5rr/AAAfQ0mv-CHKj1c63ihC-ZBca?dl=0 
%She also has a nice series of YouTube videos on efficiency in MRI studies
%that you might want to check out: https://www.youtube.com/watch?v=FD4ztsoYvSY&list=TLPQMDcwNDIwMjK8Dkl-HxtRFw&index=1

%In what follows, we want to compare the efficiency for two
%different designs: in the first design, we use the roving oddball paradigm
%(i.e., 1 trial = 1 dev + 2/11 std); 
%in the second, a classic version of the oddball paradigm (1 trial = 4 std + dev)

%We want to see if randomizing the repetition of std brings significant benefits in
%terms of efficiency to our design.

%For more information on our design, paradigm and stimuli used, please look at
%the readme file

%To run this script, we need 

%1) To run the fuction "new" (once for the roving and once for the classic oddball), to generate the 
%onset times of our two conditions: standards (std) and deviants (dev) 
%The function is enclosed in the repository

%2) matrices of contrasts: i.e., how we want to contrast this two
%conditions (remember that efficiency values are specific to a given
%contrast)

%3)other parameters of our experiment (TR, total duration etc)

%% Generation of onsets for the 1st design (Roving oddball)
%Let's generate std and dev onsets for our first design,
%in which we use the Roving Oddball paradigm. We need to estimate a distribuition of onsets, since 
%number of std repetitions are randomized and iti and the lenght of silence blocks are jittered

nsim = 1000;
test_set = cell(1,nsim); 
e = ODDBALL.new('Roving', 'abba');

for k=1:nsim
    test_set{1,k} = ODDBALL.new('Roving', 'abba')
end

onset_std_roving = cell(1,nsim);
onset_dev_roving = cell(1,nsim);

for k=1:nsim
    
    onset_std_roving{1,k} = (test_set{1,k}.onset(test_set{1,k}.action == 's')/1000);
    onset_dev_roving{1,k} = (test_set{1,k}.onset(test_set{1,k}.action == 'd')/1000);
    
end

%Since it takes a lot time to run 1000 simulations, I uploaded the
%onsets (dev/std) for both designs in the repository. So if you don't want to
%wait:

load('Onsets_Roving.mat')


%to visualize (one of) the design (zoom in to see how trials are composed):
figure();
plot(onset_dev_roving{1,1}, ones(1, numel(onset_dev_roving{1,1})), '+', onset_std_roving{1,1}, ones(1, numel(onset_std_roving{1,1})), '.r')

%% Efficiency analysis for 1st design
%let's compute the efficiency for each of the nsim of onsets
%some parameters
TR=2; %in s
total_lenght = 900; %total lenght of our experiment in s 

% contrasts
c1=[1 0]; % main effect std 
c2=[0 1]; % main effect dev
c3 = [-1 1]; %std - dev

%We first need to create each trial in high resolution. We chose the subsampling time resolution used in SPM
% i.e, 1/16th of the TR (here, 0.1250), then we convolve each trial and downsample to the TR. 

t=0:0.1250:total_lenght; %time vector in the resolution of the convolution space

% set up the hrf info
hrf_25=spm_hrf(0.1250); %funtion spm_hrf enclosed in the repository
figure()
plot(hrf_25)

%initialize efficiency 
eff_std_roving=zeros(nsim,1);
eff_dev_roving=zeros(nsim,1);
eff_diff_roving=zeros(nsim,1);

for j=1:nsim
    
    %first regressor
    t1=onset_std_roving{1,j};
    r1=zeros(1, 7201);  %we are creating a vector of zeros of total_lenght * 4 TRs
    %since we are assuming time resoultion of 0.1250 s
  
    for i=1:length(t1)
    %for each stimulus, we are filling the vector of zeros with ones
    %(onset of the stimulus + we add duration of the stimulus,
    %always 0.05s)
    r1(t1(i)<=t & t<=(t1(i)+0.05))=1;
    end
    
    %convolving with hrf and then downsampling first regressor 
    r1=conv(hrf_25, r1);
    r1=r1(1:8*TR:7200);
    
    % now we repeat the same procedure for our second conditon: deviant
    % events
    t2 = onset_dev_roving{1,j};
    r2 = zeros(1, 7201);
  
    for i=1:length(t2)
    r2(t2(i)<= t & t<=(t2(i)+0.05))=1; 
    end
    
    r2=conv(hrf_25, r2);
    r2=r2(1:8*TR:7200);
    
    %Mean centering our regressors
    r1=r1-mean(r1);
    r2=r2-mean(r2);
     
    %Efficiency for each regressor and their difference 
    X=[r1', r2'];
    eff_std_roving(j,1)=1./(c1*inv(X'*X)*c1'); %only std
    eff_dev_roving(j,1)=1./(c2*inv(X'*X)*c2'); %only dev
    eff_diff_roving(j,1)=1./(c3*inv(X'*X)*c3'); %diff(std,dev)
end

%% PLOTTING Regressors and Efficiency distribuitions

%You can plot convolved regressors of e.g. last simulation: blocks containing dev are in green
%and blocks containing only std are in blue
t_tr=t(1:8*TR:7200);  %this is time in seconds (for plotting purposes)
figure()
plot(t_tr, r1)
hold on
plot(t_tr, r2, 'g')
hold off

%We plot efficiency distribuitions for the std effect, the dev one and the difference between
%the two. We can see that the efficiency for the characterization of the std response 
%is much better than for the characterization of dev or
%different std/dev. This is because in every oddball paradigm there are 
%always more standard trials than deviants, resulting in a better efficiency
%for the standard response. 

figure()
G = [ones(size(eff_std_roving));  2*ones(size(eff_dev_roving)); 3*ones(size(eff_diff_roving))];
X = [eff_std_roving; eff_dev_roving; eff_diff_roving];
boxplot(X,G,'notch','on','Colors','rbgm','labels',{'eff_std_roving','eff_dev_roving', 'eff_diff_roving'});
title('Roving oddball: efficiency')
xlabel('Contrasts')
ylabel('Efficiency Values')

% if we plot the three distributions of the eff values separately for each
% contrast, we can see in fact that for the std effect reaches well up to 5.4723

figure()
subplot(3,1,1)
histogram(eff_std_roving, 20,'FaceColor','r')
title('Eff Std Roving')
xlabel('Efficiency Values')
subplot(3,1,2)
histogram(eff_dev_roving, 20, 'FaceColor','b')
title('Eff Dev Roving')
xlabel('Efficiency Values')
subplot(3,1,3)
histogram(eff_diff_roving, 20, 'FaceColor','m')
title('Eff Diff Roving')
xlabel('Efficiency Values')


%Let's plot then efficiency for dev effect and difference std/dev
figure()
G = [ones(size(eff_dev_roving));  2*ones(size(eff_diff_roving))];
X = [eff_dev_roving; eff_diff_roving];
boxplot(X,G,'notch','on','Colors','rbgm','labels',{'eff_dev_roving','eff_diff_roving'});
title('Roving oddball: efficiency')
xlabel('Contrasts')
ylabel('Efficiency Values')

% Let's plot the efficiency distributions for dev effect and std/dev 
%difference overlaid on each other

figure()    
% histogram(eff_std_roving, 20, 'FaceColor','g', 'FaceAlpha', 0.3)
% hold on
histogram(eff_dev_roving, 20, 'FaceColor','r', 'FaceAlpha', 0.3)    
hold on
histogram(eff_diff_roving, 20, 'FaceColor','b', 'FaceAlpha', 0.3)    
legend('Deviant','Diff std/dev')

%% Generation of onsets for the 2nd design (Classic oddball)
%Let's generate std and dev onsets for our second design,
%in which we use a version of the Classic Oddball paradigm. We need to estimate a distribuition of onsets, since, 
%also here, iti and the lenght of silence blocks are jittered

nsim = 1000;
test_set = cell(1,nsim); 
e = ODDBALL.new('Classic', 'abba');

for k=1:nsim
    test_set{1,k} = ODDBALL.new('Classic', 'abba')
end

onset_std_classic = cell(1,nsim);
onset_dev_classic = cell(1,nsim);

for k=1:nsim
    
    onset_std_classic{1,k} = (test_set{1,k}.onset(test_set{1,k}.action == 's')/1000);
    onset_dev_classic{1,k} = (test_set{1,k}.onset(test_set{1,k}.action == 'd')/1000);
    
    freq_std = e.freq(e.action == 's');
    freq_dev = e.freq(e.action == 'd');
end

%Since it takes a lot time to run 1000 simulations, I uploaded the
%onsets (dev/std) for both designs in the repository. So if you don't want to
%wait:

load('Onsets_Classic.mat')

%to visualize (one of) the design (zoom in to see how trials are composed):
figure();
plot(onset_dev_classic{1,1}, ones(1, numel(onset_dev_classic{1,1})), '+', onset_std_classic{1,1}, ones(1, numel(onset_std_classic{1,1})), '.r')

%% Efficiency analysis for 2nd design
%same procedure as before

%Initialize efficiency 
eff_std_classic=zeros(nsim,1);
eff_dev_classic=zeros(nsim,1);
eff_diff_classic=zeros(nsim,1);

for j=1:nsim
    
    %first regressor
    t1_c=onset_std_classic{1,j};
    r1_c=zeros(1, 7201);  %we are creating a vector of zeros of total_lenght * 4 TRs
    %since we are assuming time resoultion of 0.1250 s
  
    for i=1:length(t1_c)
    r1_c(t1_c(i)<=t & t<=(t1_c(i)+0.05))=1;
    end
    
    %convolving with hrf and then downsampling first regressor 
    r1_c=conv(hrf_25, r1_c);
    r1_c=r1_c(1:8*TR:7200);
    
    % now we repeat the same procedure for our second conditon: deviant
    % events
    t2_c = onset_dev_classic{1,j};
    r2_c = zeros(1, 7201);
  
    for i=1:length(t2_c)
    r2_c(t2_c(i)<= t & t<=(t2_c(i)+0.05))=1; 
    end
    
    r2_c=conv(hrf_25, r2_c);
    r2_c=r2_c(1:8*TR:7200);
    
    %Mean centering our regressors
    r1_c=r1_c-mean(r1_c);
    r2_c=r2_c-mean(r2_c);
     
    %Efficiency for each regressor and their difference 
    X=[r1_c', r2_c'];
    eff_std_classic(j,1)=1./(c1*inv(X'*X)*c1'); %only std
    eff_dev_classic(j,1)=1./(c2*inv(X'*X)*c2'); %only dev
    eff_diff_classic(j,1)=1./(c3*inv(X'*X)*c3'); %diff(std,dev)
end

%% PlOTS: comparing the two designs
%In this study we are mainly interested in the efficiency for the 3rd contrast
%(std-dev). Let's plot then the efficiency distribuitions of the (contrast) difference std/dev 
%for the classic vs roving design

figure()
G = [ones(size(eff_diff_roving));  2*ones(size(eff_diff_classic))];
X = [eff_diff_roving; eff_diff_classic];
boxplot(X,G,'notch','on','Colors','rbgm','labels',{'eff_diff_roving','eff_diff_classic'});
title('Efficiency std-dev: Classic vs Roving oddball')
xlabel('Type of oddball')
ylabel('Efficiency Values')

% The classic oddball seems to be much better in terms of efficiency for bringing 
%out the difference between std and dev

%Let's look at their distributions, separately...

figure()
subplot(2,1,1)
histogram(eff_diff_roving, 20,'FaceColor','r')
title('Eff Diff Roving')
xlabel('Efficiency Values')
subplot(2,1,2)
histogram(eff_diff_classic, 20, 'FaceColor','b')
title('Eff Diff Classic')
xlabel('Efficiency Values')


%...and overlaid
figure()    
histogram(eff_diff_roving, 20, 'FaceColor','r', 'FaceAlpha', 0.3)    
hold on
histogram(eff_diff_classic, 20, 'FaceColor','b', 'FaceAlpha', 0.3)
legend('Roving','Classic')

%We clearly have a winner!!
