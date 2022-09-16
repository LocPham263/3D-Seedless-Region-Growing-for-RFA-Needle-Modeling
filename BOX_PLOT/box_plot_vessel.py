import matplotlib.pyplot as plt
import csv
import os
# LITS
nn_unet_csv = 'C:/Users/TheThuan/Desktop/result_val_needle_500/val_vessel_decathon_nnunet.csv'
resunet_csv = 'C:/Users/TheThuan/Desktop/result_val_needle_500/RFA/val_EMC_vessel_nnunet.csv'
# save box plots
liver_figure = 'D:/SAN_PHAM_HOAN_THIEN/box_plot/vessel/'

# nn_unet csv
with open(nn_unet_csv) as f:
    reader_nn = csv.reader(f)
    nn = [row_nn for row_nn in reader_nn]
nn_hoandoi = [list(x) for x in zip(*nn)]

data_nn_fnr = nn_hoandoi[5]
data_nn_fnr.pop(0)
data_nn_fpr = nn_hoandoi[6]
data_nn_fpr.pop(0)
data_nn_ac = nn_hoandoi[3]
data_nn_ac.pop(0)

data_nn_fnr = [float(x) for x in data_nn_fnr]
data_nn_fpr = [float(x) for x in data_nn_fpr]
data_nn_ac = [float(x) for x in data_nn_ac]

# resunet csv
with open(resunet_csv) as p:
    reader_re = csv.reader(p)
    re = [row_re for row_re in reader_re]
re_hoandoi = [list(x) for x in zip(*re)]

data_re_fnr = re_hoandoi[5]
data_re_fnr.pop(0)
data_re_fpr = re_hoandoi[6]
data_re_fpr.pop(0)
data_re_ac = re_hoandoi[3]
data_re_ac.pop(0)

data_re_fnr = [float(x) for x in data_re_fnr]
data_re_fpr = [float(x) for x in data_re_fpr]
data_re_ac = [float(x) for x in data_re_ac]

data_nn = []

data_nn.append(data_nn_fnr)
data_nn.append(data_re_fnr)
data_nn.append(data_nn_fpr)
data_nn.append(data_re_fpr)

data_ac = []
data_ac.append(data_nn_ac)
data_ac.append(data_re_ac)

labels1 = ['FNR Decathlon', 'FNR EMC_NII_RFA', 'FPR Decathlon', 'FPR EMC_NII_RFA']
labels2 = ['IOU Decathlon', 'IOU EMC_NII_RFA']

colors1 = ['lightgreen', 'lightgreen', 'lightblue', 'lightblue']
colors2 = ['green', 'blue']

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))

# rectangular box plot
bplot1 = ax1.boxplot(data_nn,
                     vert=True,  # vertical box alignment
                     patch_artist=True,  # fill with color
                     labels=labels1)  # will be used to label x-ticks
# ax1.set_title('Rectangular box plot') # up name

ax1.set_ylabel('Value',fontsize=18) # don vi y
for patch, color in zip(bplot1['boxes'], colors1):
    patch.set_facecolor(color)
ax1.yaxis.grid(True)
bplot2 = ax2.boxplot(data_ac,
                     vert=True,  # vertical box alignment
                     patch_artist=True,  # fill with color
                     labels=labels2)  # will be used to label x-ticks

ax2.set_ylabel('Value',fontsize=18) # don vi y
for patch, color in zip(bplot2['boxes'], colors2):
    patch.set_facecolor(color)
ax2.yaxis.grid(True)

plt.sca(ax1)
plt.xticks(fontsize=11)
plt.yticks(fontsize=18)

plt.sca(ax2)
plt.xticks(fontsize=11)
plt.yticks(fontsize=18)

plt.show()
fig.savefig(os.path.join(liver_figure, 'vessel_decalthon.png'), dpi=600)