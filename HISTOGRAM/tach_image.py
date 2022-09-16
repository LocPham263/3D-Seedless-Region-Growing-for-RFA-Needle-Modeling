import os
import SimpleITK as sitk
from tqdm import tqdm
import numpy as np
'''
đổi tên liver labels
'''
# liver_label = 'D:/EMC_GT/liver_GT/'
# liver_save = 'D:/SAN_PHAM_HOAN_THIEN/histogram/liver_label/'
#
# for file in tqdm(os.listdir(liver_label)):
#     liver_itk = sitk.ReadImage(os.path.join(liver_label, file))
#     sitk.WriteImage(liver_itk, os.path.join(liver_save, file.replace('_liver_seg.nii.gz','.nii.gz')))

'''
tách vùng gan
tách vùng kim
'''
ct_folder = 'D:/lits_liver challenge/needle_RFA/Neddle_Data/EMC_NII_RFA_Needle/'
liver_label = 'D:/SAN_PHAM_HOAN_THIEN/histogram/liver_label/'
needle_folder = 'D:/lits_liver challenge/needle_RFA/Neddle_Data/Needle_Segmentation/'

liver_needle_image_folder = 'D:/SAN_PHAM_HOAN_THIEN/histogram/liver_con_kim/'
needle_image_folder = 'D:/SAN_PHAM_HOAN_THIEN/histogram/needle_image/'
liver_del_needle_folder = 'D:/SAN_PHAM_HOAN_THIEN/histogram/liver_xoa_kim/'

for file in tqdm(os.listdir(liver_label)):

    ct_itk = sitk.ReadImage(os.path.join(ct_folder, file))
    liver_itk = sitk.ReadImage(os.path.join(liver_label, file))
    needle_itk = sitk.ReadImage(os.path.join(needle_folder, file))

    ct_array = sitk.GetArrayFromImage(ct_itk)
    liver_array = sitk.GetArrayFromImage(liver_itk)
    needle_array = sitk.GetArrayFromImage(needle_itk)

    # liver and needle
    mask_ln = ct_array.copy()
    mask_n = ct_array.copy()

    mask_ln[liver_array == 0] = 0
    mask_l = mask_ln.copy()
    mask_l[needle_array == 1] = 0
    mask_n[needle_array == 0] = 0

    new_ln = sitk.GetImageFromArray(mask_ln)
    new_ln.SetOrigin(ct_itk.GetOrigin())
    new_ln.SetSpacing(ct_itk.GetSpacing())

    new_l = sitk.GetImageFromArray(mask_l)
    new_l.SetOrigin(ct_itk.GetOrigin())
    new_l.SetSpacing(ct_itk.GetSpacing())

    new_n = sitk.GetImageFromArray(mask_n)
    new_n.SetOrigin(ct_itk.GetOrigin())
    new_n.SetSpacing(ct_itk.GetSpacing())

    sitk.WriteImage(new_ln, os.path.join(liver_needle_image_folder, file))
    sitk.WriteImage(new_l, os.path.join(liver_del_needle_folder, file))
    sitk.WriteImage(new_n, os.path.join(needle_image_folder, file))