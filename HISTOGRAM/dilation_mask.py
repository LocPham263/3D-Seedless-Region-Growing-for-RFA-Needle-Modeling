import SimpleITK as sitk
import numpy as np
import os
import shutil


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

ct_folder = 'D:/lits_liver challenge/needle_RFA/Neddle_Data/EMC_NII_RFA_Needle/p014_inter_ar_006.nii.gz'
needle_label_folder = 'D:/lits_liver challenge/needle_RFA/Neddle_Data/Needle_Segmentation/p014_inter_ar_006.nii.gz'
save_folder = 'D:/SAN_PHAM_HOAN_THIEN/histogram/extend_label/p014_inter_ar_006_Rect.nii.gz'

ct_itk = sitk.ReadImage(ct_folder)
needle_itk = sitk.ReadImage(needle_label_folder)

ct_array = sitk.GetArrayFromImage(ct_itk)
needle_array = sitk.GetArrayFromImage(needle_itk)

Radius_Size = 4
Kernel_Type = 'Rect'
segment_Morphologi = dilation_morpologi(needle_itk,Kernel_Type,[Radius_Size,Radius_Size,1])

# new_image = sitk.GetImageFromArray(segment_Morphologi)
# new_image.GetSpacing(ct_itk.GetSpacing())
# new_image.GetOrigin(ct_itk.GetOrigin())
# sitk.WriteImage(segment_Morphologi, save_folder)

