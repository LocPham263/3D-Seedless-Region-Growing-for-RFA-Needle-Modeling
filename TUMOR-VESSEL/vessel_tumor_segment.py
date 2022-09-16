import SimpleITK as sitk
import numpy as np
import subprocess
import os
import sys
sys.path.append(os.path.split(sys.path[0])[0])
import shutil

folder_save_file = '/media/avitech-pc-5500/New Volume/NEEDLE_DATA/test_subprocess/'
ct_dir = '/media/avitech-pc-5500/New Volume/NEEDLE_DATA/EMC_NII_RFA_Needle/p037_inter_pv_008.nii.gz'
file_name = 'p037_inter_pv_008.nii.gz'

if os.path.exists(folder_save_file):
    shutil.rmtree(folder_save_file)

new_ct_path = os.path.join(folder_save_file,'ct')
new_seg_path = os.path.join(folder_save_file,'seg')

os.mkdir(folder_save_file)
os.mkdir(new_ct_path)
os.mkdir(new_seg_path)

# load data
ct = sitk.ReadImage(ct_dir)
# save 0000
sitk.WriteImage(ct, os.path.join(new_ct_path,file_name.replace('.nii.gz','_0000.nii.gz')))

cmd = ["nnUNet_predict -i /media/avitech-pc-5500/New\ Volume/NEEDLE_DATA/test_subprocess/ct/ -o /media/avitech-pc-5500/New\ Volume/NEEDLE_DATA/test_subprocess/seg/ -m 3d_fullres -t 8"]
result = subprocess.run(cmd, shell=True)

seg = sitk.ReadImage(os.path.join(new_seg_path,file_name))
seg_array = sitk.GetArrayFromImage(seg)

tumor_seg = np.zeros_like(seg_array)
vessel_seg = np.zeros_like(seg_array)

tumor_seg[seg_array == 2] = 1
vessel_seg[seg_array == 1] = 1

tumor = sitk.GetImageFromArray(tumor_seg)
tumor.SetDirection(ct.GetDirection())
tumor.SetOrigin(ct.GetOrigin())
tumor.SetSpacing(ct.GetSpacing())
sitk.WriteImage(tumor, os.path.join(new_seg_path,file_name.replace('.nii.gz','_tumor.nii.gz')))

vessel = sitk.GetImageFromArray(vessel_seg)
vessel.SetDirection(ct.GetDirection())
vessel.SetOrigin(ct.GetOrigin())
vessel.SetSpacing(ct.GetSpacing())
sitk.WriteImage(vessel, os.path.join(new_seg_path,file_name.replace('.nii.gz','_vessel.nii.gz')))



