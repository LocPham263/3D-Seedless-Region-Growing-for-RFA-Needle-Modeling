# segment needle

import SimpleITK as sitk
import numpy as np
import os
from tqdm import tqdm
import needle_segment

ct_path = 'D:/lits_liver challenge/Needle_Data/data_needle_ANH_LOC/EMC_NII_RFA_Needle/'
seg_save_path = 'D:/lits_liver challenge/Needle_Data/THETHUAN_NEEDLE_SEG_750/'
liver_seg_path = 'D:/lits_liver challenge/Needle_Data/data_needle_ANH_LOC/Liver_Seg/'
seg_fix_name = 'D:/lits_liver challenge/Needle_Data/Needle_Seg_700/'

ct_ls = os.listdir(ct_path)
liver_ls = os.listdir(liver_seg_path)

def NEEDLE_SEG():
    for i in tqdm(range(len(ct_ls))):
        ct = sitk.ReadImage(ct_path + ct_ls[i])
        ct_array = sitk.GetArrayFromImage(ct)

        liver = sitk.ReadImage(liver_seg_path + os.path.splitext(os.path.splitext(ct_ls[i])[0])[0] + '_liver_seg.nii.gz')
        liver_array = sitk.GetArrayFromImage(liver)
        mask = ct_array * liver_array

        idx = needle_segment.get_idx(mask)
        if mask[idx[0], idx[1], idx[2]] < 300:
            idx = needle_segment.get_idx(ct_array)

        ct_array[ct_array < 750] = 0
        ct_array[ct_array >= 750] = 1

        ct_array = needle_segment.grow(ct_array, (idx[0], idx[1], idx[2]), 5).astype(np.int16)

        needle_seg = sitk.GetImageFromArray(ct_array)
        needle_seg.SetOrigin(ct.GetOrigin())
        needle_seg.SetSpacing(ct.GetSpacing())
        sitk.WriteImage(needle_seg, seg_save_path + ct_ls[i])

def fix_name():
    seg_ls = os.listdir(seg_fix_name)

    for i in tqdm(range(len(seg_ls))):
        needle = sitk.ReadImage(seg_fix_name + seg_ls[i])
        sitk.WriteImage(needle, seg_save_path + ct_ls[i])

# fix_name()
NEEDLE_SEG()