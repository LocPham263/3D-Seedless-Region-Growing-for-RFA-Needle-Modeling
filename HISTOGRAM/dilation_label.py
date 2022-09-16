import SimpleITK as sitk
import shutil
import os
import numpy

def dilation_morpologi(Image, mask_dilation_kernel, mask_dilation_radius):
    dilater = sitk.BinaryDilateImageFilter()
    dilater.SetKernelType(eval("sitk.sitk" + mask_dilation_kernel))
    dilater.SetKernelRadius(mask_dilation_radius)
    result_Morphologi = dilater.Execute(Image)
    return result_Morphologi

ct_path = 'D:/SAN_PHAM_HOAN_THIEN/test_dilation_liver/ct/'
seg_path = 'D:/SAN_PHAM_HOAN_THIEN/test_dilation_liver/seg/'
save_path = 'D:/SAN_PHAM_HOAN_THIEN/test_dilation_liver/save/'
file_name = 'p031_inter_pv_003.nii.gz'

seg = sitk.ReadImage(os.path.join(seg_path, file_name))

Radius_Size = 1
Kernel_Type = 'Ball'
segment_Morphologi = dilation_morpologi(seg,Kernel_Type,[Radius_Size,Radius_Size,1])

# new_image = sitk.GetImageFromArray(segment_Morphologi)
# segment_Morphologi.GetSpacing(seg.GetSpacing())
# segment_Morphologi.GetOrigin(seg.GetOrigin())
sitk.WriteImage(segment_Morphologi, os.path.join(save_path, file_name.replace('.nii.gz', '_Ball.nii.gz')))

