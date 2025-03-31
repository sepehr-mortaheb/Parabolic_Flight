#!/bin/bashs

directory=/home/smortaheb/Projects/PF/data/raw

cd ${directory}

subjects=`ls | grep sub`

for subj in ${subjects};
do
    cd ${directory}/${subj}
    sessions=`ls | grep ses`
    for ses in ${sessions};
    do 
        func=${directory}/${subj}/${ses}/func/${subj}_${ses}_task-rest_acq-main_bold.nii
        PE1=${directory}/${subj}/${ses}/func/${subj}_${ses}_task-rest_acq-TUPA1_bold.nii
        PE2=${directory}/${subj}/${ses}/func/${subj}_${ses}_task-rest_acq-TUPA2_bold.nii
        mrcat ${PE1} ${PE2} ${directory}/${subj}/${ses}/func/${subj}_${ses}_task-rest_acq-TUPA_bold.nii
        PE=${directory}/${subj}/${ses}/func/${subj}_${ses}_task-rest_acq-TUPA_bold.nii

        mkdir -p ${directory}/${subj}/${ses}/func/tmp
        out_dir=${directory}/${subj}/${ses}/func/tmp
        cp ${func} ${out_dir}
        cp ${PE} ${out_dir}

        cd ${out_dir}

        echo "${subj}, ${ses}: Functional data Realignment ... "
        mcflirt -in ${func} -out rafunc -plots -meanvol -spline_final
        cp rafunc.par swmsc${subj}_${ses}_task-rest_dir-AP_bold.par
        rm rafunc.par

        echo "${subj}, ${ses}: Phase encoded data realignment ... "
        mcflirt -in ${PE} -reffile rafunc_mean_reg -out raPE -plots -spline_final

        echo "${subj}, ${ses}: Extraction of first functional volume ... "  
        fslroi rafunc rafunc_blipup 0 1 

        echo "${subj}, ${ses}: Extraction of first phase encoded volume ... "
        fslroi raPE raPE_blipdn 0 1 

        echo "${subj}, ${ses}: Merging the two extracted volumes ... "
        fslmerge -t blip_updn rafunc_blipup raPE_blipdn

        echo "${subj}, ${ses}: Creating TOPUP data file ... "
        echo "0 1 0 0.0406707" > ./topup_acq_param.txt 
        echo "0 -1 0 0.0406707"  >> ./topup_acq_param.txt

        echo "${subj}, ${ses}: Performing TOPUP ... "
        topup --imain=blip_updn --datain=topup_acq_param.txt --config=b02b0.cnf --out=blip_topup

        echo "${subj}, ${ses}: Splitting 4D functional data into 3D volumes ... "
        fslsplit rafunc vol -t

        echo "${subj}, ${ses}: Apply TOPUP on the functional 3D volumes ... "
        for tt in $(ls -1 ./vol*.nii.gz); 
        do
            applytopup --imain=${tt} --inindex=1 --datain=topup_acq_param.txt  --method=jac --topup=blip_topup --out=${tt/.nii.gz/_topup.nii.gz}
        done

        echo "${subj}, ${ses}: Merging topuped 3D volumes into a single 4D volume ... "
        fslmerge -t mscfunc  vol*_topup*.nii.gz

        echo "${subj}, ${ses}: Removing unnecessary files ... "
        rm -f topup_acq_param.txt  vol*.nii.gz *_log blip* ra*

        cp mscfunc.nii.gz msc${subj}_${ses}_task-rest_dir-AP_bold.nii.gz
        rm -f mscfunc.nii.gz 
        gunzip msc${subj}_${ses}_task-rest_dir-AP_bold.nii.gz
        rm -f msc${subj}_${ses}_task-rest_dir-AP_bold.nii.gz

        fslmaths msc${subj}_${ses}_task-rest_dir-AP_bold.nii -Tmean mean_${subj}_${ses}_task-rest_dir-AP_bold.nii
        gunzip mean_${subj}_${ses}_task-rest_dir-AP_bold.nii.gz
        rm -f mean_${subj}_${ses}_task-rest_dir-AP_bold.nii.gz


        echo "Done!"
    done
done