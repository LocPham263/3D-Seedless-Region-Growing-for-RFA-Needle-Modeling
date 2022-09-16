"""
chuẩn bị dữ liệu :
hợp label : chỉ còn liver label
giới hạn ngưỡng : -200 200
chuẩn hóa khoảng cách : 1mm
tính vùng slide chứa liver : start end

áp dụng hoàn thiện cho bộ LiTS

"""
import os
import sys
sys.path.append(os.path.split(sys.path[0])[0])
import shutil
from time import time
import numpy as np
from tqdm import tqdm
import SimpleITK as sitk
import scipy.ndimage as ndimage
import parameter as para

if os.path.exists(para.train_path):
    shutil.rmtree(para.train_path)

new_ct_path = os.path.join(para.train_path, 'ct')
new_seg_path = os.path.join(para.train_path, 'seg')

os.mkdir(para.train_path)
os.mkdir(new_ct_path)
os.mkdir(new_seg_path)

start = time()
for file in tqdm(os.listdir(para.ct_path)):
    # đọc ảnh ct và chuyển sang dạng array
    ct = sitk.ReadImage(os.path.join(para.ct_path, file), sitk.sitkInt16)
    ct_array = sitk.GetArrayFromImage(ct)
    # đọc ảnh seg và chuyển sang dạng array
    seg = sitk.ReadImage(os.path.join(para.seg_path, file.replace('volume', 'segmentation')), sitk.sitkUInt8)
    seg_array = sitk.GetArrayFromImage(seg)
    # hợp tumor label vào liver label
    seg_array[seg_array > 0] = 1
    # giới hạn ngưỡng từ -200 đến 200
    ct_array[ct_array > para.up] = para.up
    ct_array[ct_array < para.low] = para.low
    # chuẩn hóa khoảng cách các slice 1mm
    ct_array = ndimage.zoom(ct_array, (ct.GetSpacing()[-1] / para.slice_thickness, para.down_scale, para.down_scale), order=3)
    seg_array = ndimage.zoom(seg_array, (ct.GetSpacing()[-1] / para.slice_thickness, 1, 1), order=0)
    # tìm slide bắt đầu là kêt thúc chứa liver
    z = np.any(seg_array, axis=(1, 2))
    start_slice, end_slice = np.where(z)[0][[0, -1]]

    start_slice = max(0, start_slice - para.expand_slice)
    end_slice = min(seg_array.shape[0] - 1, end_slice + para.expand_slice)

    if end_slice - start_slice + 1 < para.size_block:
        print('!!!!!!!!!!!!!!!!')
        print(file, 'have too little slice', ct_array.shape[0])
        print('!!!!!!!!!!!!!!!!')
        continue

    ct_array = ct_array[start_slice:end_slice + 1, :, :]
    seg_array = seg_array[start_slice:end_slice + 1, :, :]

    new_ct = sitk.GetImageFromArray(ct_array)

    new_ct.SetDirection(ct.GetDirection())
    new_ct.SetOrigin(ct.GetOrigin())
    new_ct.SetSpacing((ct.GetSpacing()[0] * int(1 / para.down_scale), ct.GetSpacing()[1] * int(1 / para.down_scale), para.slice_thickness))

    new_seg = sitk.GetImageFromArray(seg_array)

    new_seg.SetDirection(ct.GetDirection())
    new_seg.SetOrigin(ct.GetOrigin())
    new_seg.SetSpacing((ct.GetSpacing()[0], ct.GetSpacing()[1], para.slice_thickness))

    sitk.WriteImage(new_ct, os.path.join(new_ct_path, file))
    sitk.WriteImage(new_seg, os.path.join(new_seg_path, file.replace('volume', 'segmentation').replace('.nii', '.nii.gz')))
