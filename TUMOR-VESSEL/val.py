import shutil
import numpy as np
import SimpleITK as sitk
import cv2
import matplotlib.pyplot as plt
import os
import metrics
from tqdm import tqdm
import pandas as pd
from skimage import morphology
from scipy import ndimage

tumor_seg = ''
tumor_labels = ''
vessel_seg = ''
vessel_label = ''

def eval():
    file_name = []
    DSC_val = []
    IoU_val = []
    VOE_val = []
    RVD_val = []
    FNR_val = []
    FPR_val = []
    ASSD_val = []
    RMSD_val = []
    MSD_val = []

    for i in tqdm(range(len(seg_ls))):
        seg_sitk = sitk.ReadImage(BASE_DIR + seg_folder + seg_ls[i])
        seg = sitk.GetArrayFromImage(seg_sitk)

        label_sitk = sitk.ReadImage(BASE_DIR + label_folder + label_ls[i])
        label = sitk.GetArrayFromImage(label_sitk)


        Loss = metrics.Metric(label, seg, label_sitk.GetSpacing())
        print(seg_ls[i] + ': ' + str(Loss.get_dice_coefficient()))
        DSC = Loss.get_dice_coefficient()
        IoU = Loss.get_jaccard_index()
        VOE = Loss.get_VOE()
        FNR = Loss.get_FNR()
        FPR = Loss.get_FPR()
        ASSD = Loss.get_ASSD()
        RMSD = Loss.get_RMSD()
        MSD = Loss.get_MSD()

        file_name.append(seg_ls[i])
        DSC_val.append(DSC)
        IoU_val.append(IoU)
        VOE_val.append(VOE)
        FNR_val.append(FNR)
        FPR_val.append(FPR)
        ASSD_val.append(ASSD)
        RMSD_val.append(RMSD)
        MSD_val.append(MSD)

        df = pd.DataFrame({'File name': file_name,
                        'DSC': DSC_val,
                        'IoU': IoU_val,
                        'VOE': VOE_val,
                        'FNR': FNR_val,
                        'FPR': FPR_val,
                        'ASSD': ASSD_val,
                        'RMSD': RMSD_val,
                        'MSD': MSD_val})

        df.to_csv(path_or_buf = 'C:/Users/Admin/Desktop/Needle/seg_report_700_dilate.csv')
