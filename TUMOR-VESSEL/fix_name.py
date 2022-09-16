import SimpleITK as sitk
import os
import sys
sys.path.append(os.path.split(sys.path[0])[0])
import numpy as np
from tqdm import tqdm
import shutil
from time import time

ct_path = '/media/avitech-pc-5500/New Volume/Task08_HepaticVessel/imagesTr/'
resave_path = '/media/avitech-pc-5500/New Volume/Task08_HepaticVessel/imagesTr_0000/'

for file in tqdm(os.listdir(ct_path)):
    ct = sitk.ReadImage(os.path.join(ct_path, file))
    sitk.WriteImage(ct, os.path.join(resave_path, file.replace('.nii.gz', '_0000.nii.gz')))