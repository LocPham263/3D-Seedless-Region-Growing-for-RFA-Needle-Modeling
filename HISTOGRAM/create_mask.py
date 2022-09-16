import SimpleITK as sitk
import numpy as np
import os
from tqdm import tqdm

def dilation_morpologi(Image, mask_dilation_kernel, mask_dilation_radius):

    dilater = sitk.BinaryDilateImageFilter()
    dilater.SetKernelType(eval("sitk.sitk" + mask_dilation_kernel))
    dilater.SetKernelRadius(mask_dilation_radius)
    result_Morphologi = dilater.Execute(Image)

    return result_Morphologi

# Mask Filter
def mask_binary(Image, segment):
    Mask_image = sitk.MaskImageFilter()
    Image_Mask = Mask_image.Execute(Image,segment)
    return Image_Mask

# Subtract Image
def subtractImage(Image1, Image2):
    Subtract_Image = sitk.SubtractImageFilter()
    Image_Subtract = Subtract_Image.Execute(Image1,Image2)
    return Image_Subtract
# Add Image
def addImage(Image1, Image2):
    Add_Image = sitk.AddImageFilter()
    Image_Add = Add_Image.Execute(Image1,Image2)
    return Image_Add
# data
ct_folder = 'D:/lits_liver challenge/needle_RFA/Neddle_Data/EMC_NII_RFA_Needle/'
needle_label_folder = 'D:/lits_liver challenge/needle_RFA/Neddle_Data/Needle_Segmentation/'
liver_label_folder = 'D:/SAN_PHAM_HOAN_THIEN/histogram/liver_GT/'
list_file = 'D:/SAN_PHAM_HOAN_THIEN/histogram/needle_expand_image/'

# save label
needle_expand_label_folder = 'D:/SAN_PHAM_HOAN_THIEN/histogram/thu_hep_liver_histogram/labels/needle_expand/'
liver_thu_hep_label_folder = 'D:/SAN_PHAM_HOAN_THIEN/histogram/thu_hep_liver_histogram/labels/liver_thu_hep/'
liver_needle_thu_hep_label_folder = 'D:/SAN_PHAM_HOAN_THIEN/histogram/thu_hep_liver_histogram/labels/liver_needle_thu_hep/'

# save mask
liver_mask_folder = 'D:/SAN_PHAM_HOAN_THIEN/histogram/thu_hep_liver_histogram/mask/liver_mask/'
needle_mask_folder = 'D:/SAN_PHAM_HOAN_THIEN/histogram/thu_hep_liver_histogram/mask/needle_mask/'
liver_needle_mask_folder = 'D:/SAN_PHAM_HOAN_THIEN/histogram/thu_hep_liver_histogram/mask/liver_needle_mask/'

for file in tqdm(os.listdir(list_file)):

    ct_itk = sitk.ReadImage(os.path.join(ct_folder, file))
    needle_itk = sitk.ReadImage(os.path.join(needle_label_folder, file))
    liver_itk = sitk.ReadImage(os.path.join(liver_label_folder, file))

    liver_GT = sitk.GetArrayFromImage(liver_itk)
    needle_GT = sitk.GetArrayFromImage(needle_itk)

    needle_Radius_Size = 1
    liver_Radius_Size = 20
    Kernel_Type = 'Ball'

    """
    tạo needle label mở rộng
    tạo liver label thu hẹp
    """
    needle_expand = dilation_morpologi(needle_itk, Kernel_Type, [needle_Radius_Size, needle_Radius_Size, 1])
    liver_expand = dilation_morpologi(needle_itk, Kernel_Type, [liver_Radius_Size, liver_Radius_Size, 1])

    needle_Morphologi_array = sitk.GetArrayFromImage(needle_expand)
    liver_Morphologi_array =sitk.GetArrayFromImage(liver_expand)

    needle_Morphologi_array[liver_GT == 0] = 0

    liver_Morphologi_array[liver_GT == 0] = 0

    needle_Morphologi = sitk.GetImageFromArray(needle_Morphologi_array)
    liver_Morphologi = sitk.GetImageFromArray(liver_Morphologi_array)

    needle_Morphologi.SetOrigin(ct_itk.GetOrigin())
    needle_Morphologi.SetSpacing(ct_itk.GetSpacing())
    sitk.WriteImage(needle_Morphologi, os.path.join(needle_expand_label_folder, file))

    liver_Morphologi.SetOrigin(ct_itk.GetOrigin())
    liver_Morphologi.SetSpacing(ct_itk.GetSpacing())
    sitk.WriteImage(liver_Morphologi, os.path.join(liver_needle_thu_hep_label_folder, file))

    needle_array = sitk.GetArrayFromImage(needle_Morphologi)
    liver_needle_array = sitk.GetArrayFromImage(liver_Morphologi)

    liver_array = liver_needle_array.copy()
    liver_array[needle_array == 1] = 0

    new_liver = sitk.GetImageFromArray(liver_array)

    new_liver.SetOrigin(ct_itk.GetOrigin())
    new_liver.SetSpacing(ct_itk.GetSpacing())
    sitk.WriteImage(new_liver, os.path.join(liver_thu_hep_label_folder, file))

    """
    tạo liver mask
    tạo needle mask
    tạo liver needle mask
    """
    ct_array = sitk.GetArrayFromImage(ct_itk)

    liver_needle_mask = ct_array.copy()
    liver_mask = ct_array.copy()
    needle_mask = ct_array.copy()

    liver_needle_mask[liver_needle_array == 0] = 0
    liver_mask[liver_array == 0] = 0
    needle_mask[needle_array == 0] = 0

    liver_needle_save = sitk.GetImageFromArray(liver_needle_mask)
    liver_save = sitk.GetImageFromArray(liver_mask)
    needle_save = sitk.GetImageFromArray(needle_mask)

    liver_needle_save.SetOrigin(ct_itk.GetOrigin())
    liver_needle_save.SetSpacing(ct_itk.GetSpacing())
    sitk.WriteImage(liver_needle_save, os.path.join(liver_needle_mask_folder, file))

    liver_save.SetOrigin(ct_itk.GetOrigin())
    liver_save.SetSpacing(ct_itk.GetSpacing())
    sitk.WriteImage(liver_save, os.path.join(liver_mask_folder, file))

    needle_save.SetOrigin(ct_itk.GetOrigin())
    needle_save.SetSpacing(ct_itk.GetSpacing())
    sitk.WriteImage(needle_save, os.path.join(needle_mask_folder, file))
