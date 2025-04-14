cat split/part_* > ../rfMRI_REST1_LR_Atlas_MSMAll_hp2000_clean.dtseries.nii

expected_hash="aa60150986acfe6c492409b8026effd64f6c76e95db15256067d1a40c46aab3d"

calculated_hash=$(sha256sum ../rfMRI_REST1_LR_Atlas_MSMAll_hp2000_clean.dtseries.nii | awk '{ print $1 }')

if [ "$calculated_hash" == "$expected_hash" ]; then
    echo "true"
else
    echo "false"
fi


