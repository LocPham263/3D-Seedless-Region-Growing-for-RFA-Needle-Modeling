import matplotlib.pyplot as plt
import csv
import numpy as np
import pandas as pd

csv_path = 'D:/SAN_PHAM_HOAN_THIEN/danh_gia_seg/val/val_liver/val_liver_nn_unet.csv'
with open(csv_path) as f:
    reader = csv.reader(f)
    l = [row for row in reader]
l_hoandoi = [list(x) for x in zip(*l)]

data_dsc = l_hoandoi[2]
data_dsc.pop(0)
data_dsc.pop(41)
data_dsc.pop(40)
data_iou = l_hoandoi[3]
data_iou.pop(0)
data_iou.pop(41)
data_iou.pop(40)
data_voe = l_hoandoi[4]
data_voe.pop(0)
data_voe.pop(41)
data_voe.pop(40)
data_fnr = l_hoandoi[5]
data_fnr.pop(0)
data_fnr.pop(41)
data_fnr.pop(40)
data_fpr = l_hoandoi[6]
data_fpr.pop(0)
data_fpr.pop(41)
data_fpr.pop(40)
data_assd = l_hoandoi[7]
data_assd.pop(0)
data_assd.pop(41)
data_assd.pop(40)
data_rmsd = l_hoandoi[8]
data_rmsd.pop(0)
data_rmsd.pop(41)
data_rmsd.pop(40)
data_msd = l_hoandoi[9]
data_msd.pop(0)
data_msd.pop(41)
data_msd.pop(40)
data = []
data_dsc = [float(x) for x in data_dsc]
data_iou = [float(x) for x in data_iou]
data_voe = [float(x) for x in data_voe]
data_fnr = [float(x) for x in data_fnr]
data_fpr = [float(x) for x in data_fpr]
data_assd = [float(x) for x in data_assd]
data_rmsd = [float(x) for x in data_rmsd]
data_msd = [float(x) for x in data_msd]

# labels = ['x']
# df1 = pd.DataFrame({'col':data_msd})
# print(df1.head())

print(type(data_msd),len(data_msd),type(data_msd[1]))
data = []
# data.append(data_dsc)
# data.append(data_iou)
# data.append(data_voe)
data.append(data_fnr)
data.append(data_fpr)
# data.append(data_assd)
# data.append(data_rmsd)
# data.append(data_msd)

# print(type(data), len(data))
# labels = ['dsc', 'iou']
# data = data_msd
# labels = ['dsc']
# data = ([data_dsc], [data_iou], [data_voe], [data_fnr], [data_fpr], [data_assd], [data_rmsd], [data_msd])
labels = ['FNR', 'FPR']

print(data)
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))

# rectangular box plot
bplot1 = ax1.boxplot(data,
                     vert=True,  # vertical box alignment
                     patch_artist=True,  # fill with color
                     labels=labels)  # will be used to label x-ticks
ax1.set_title('Rectangular box plot') # up name

# notch shape box plot
bplot2 = ax2.boxplot(data,
                     notch=True,  # notch shape
                     vert=True,  # vertical box alignment
                     patch_artist=True,  # fill with color
                     labels=labels)  # will be used to label x-ticks
ax2.set_title('Notched box plot') # upper name

# fill with colors
colors = ['pink', 'lightblue', 'lightgreen']
for bplot in (bplot1, bplot2):
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)

# adding horizontal grid lines
for ax in [ax1, ax2]:
    ax.yaxis.grid(True)
    ax.set_xlabel('Three separate samples') # don vi x
    ax.set_ylabel('Observed values') # don vi y

plt.show()