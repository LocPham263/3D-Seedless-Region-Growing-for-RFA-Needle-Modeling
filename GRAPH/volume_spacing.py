import os
import numpy as np
import SimpleITK as sitk
import pandas as pd
from tqdm import tqdm

ct_lits_folder = 'D:/lits_liver challenge/LITS/CT_image/'
ct_decathlon_folder = 'F:/Task08_HepaticVessel/imagesTr/'
ct_emc_folder = 'D:/lits_liver challenge/needle_RFA/Neddle_Data/EMC_NII_RFA_Needle/'
save_spacing = 'D:/SAN_PHAM_HOAN_THIEN/spacing_data/'

spacing_x = []
spacing_y = []
spacing_z = []
name_file = []

min = 1000
max = 0

for file in tqdm(os.listdir(ct_decathlon_folder)):
    name_file.append(file)
    ct = sitk.ReadImage(os.path.join(ct_decathlon_folder, file))
    ct_array = sitk.GetArrayFromImage(ct)
    # print(ct_array.shape[0],ct_array.shape[1],ct_array.shape[2])
    if ct_array.shape[0] > max :
        max = ct_array.shape[0]
    if ct_array.shape[0] < min:
        min = ct_array.shape[0]
print(max, min)
#     spacing = ct.GetSpacing()
#     # print(spacing[0], spacing[1], spacing[2])
#     spacing_x.append(spacing[0])
#     spacing_y.append(spacing[1])
#     spacing_z.append(spacing[2])
#
# csv_spacing = pd.DataFrame({'name_file' : name_file,
#                             'spacing x' : spacing_x,
#                             'spacing y' : spacing_y,
#                             'spacing z' : spacing_z
# })
#
# # csv_spacing.to_csv(os.path.join(save_spacing, 'emc_spacing.csv'))
# csv_spacing.to_csv(os.path.join(save_spacing, 'Lits_spacing.csv'))
# # csv_spacing.to_csv(os.path.join(save_spacing, 'decathlon_spacing.csv'))



