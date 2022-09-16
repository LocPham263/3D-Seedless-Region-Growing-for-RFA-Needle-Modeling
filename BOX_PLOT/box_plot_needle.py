import matplotlib.pyplot as plt
import csv
import os
# LITS
RFA_csv = 'D:/SAN_PHAM_HOAN_THIEN\danh_gia_seg/val_many_thresh_needle/500_val.csv'
# save box plots
RFA_figure = 'D:/SAN_PHAM_HOAN_THIEN/box_plot/needle/'

# nn_unet csv
with open(RFA_csv) as f:
    reader_RFA = csv.reader(f)
    RFA = [row_nn for row_nn in reader_RFA]
RFA_hoandoi = [list(x) for x in zip(*RFA)]

data_RFA_fnr = RFA_hoandoi[3]
data_RFA_fnr.pop(0)
data_RFA_fpr = RFA_hoandoi[4]
data_RFA_fpr.pop(0)
data_RFA_ac = RFA_hoandoi[2]
data_RFA_ac.pop(0)

data_RFA_fnr = [float(x) for x in data_RFA_fnr]
data_RFA_fpr = [float(x) for x in data_RFA_fpr]
data_RFA_ac = [float(x) for x in data_RFA_ac]

data_RFA = []
data_RFA.append(data_RFA_fnr)
data_RFA.append(data_RFA_fpr)
data_acc = []
data_acc.append(data_RFA_ac)

labels1 = ['FNR', 'FPR']
labels2 = ['DSC']

colors1 = ['lightgreen', 'lightblue', 'blue']
colors2 = ['blue']

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))

# rectangular box plot
bplot1 = ax1.boxplot(data_RFA,
                     vert=True,  # vertical box alignment
                     patch_artist=True,  # fill with color
                     labels=labels1)  # will be used to label x-ticks
# ax1.set_title('Rectangular box plot') # up name
ax1.yaxis.grid(True)
ax1.set_ylabel('Value',fontsize=18) # don vi y
for patch, color in zip(bplot1['boxes'], colors1):
    patch.set_facecolor(color)

# rectangular box plot
bplot2 = ax2.boxplot(data_acc,
                     vert=True,  # vertical box alignment
                     patch_artist=True,  # fill with color
                     labels=labels2)  # will be used to label x-ticks
# ax2.set_title('Rectangular box plot') # up name

ax2.set_ylabel('Value',fontsize=18) # don vi y
for patch, color in zip(bplot2['boxes'], colors2):
    patch.set_facecolor(color)
ax2.yaxis.grid(True)
plt.sca(ax1)
plt.xticks(fontsize=14)
plt.yticks(fontsize=18)

plt.sca(ax2)
plt.xticks(fontsize=14)
plt.yticks(fontsize=18)
plt.show()
# fig.savefig(os.path.join(RFA_figure, 'needle_RFA.png'), dpi=600)