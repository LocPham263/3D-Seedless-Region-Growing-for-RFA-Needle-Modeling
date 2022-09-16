import os
import shutil
import numpy as np
import SimpleITK as sitk

import matplotlib.pyplot as plt
from tqdm import tqdm

liver_needle_folder = 'D:/SAN_PHAM_HOAN_THIEN/histogram/liver_con_kim/'
liver_folder = 'D:/SAN_PHAM_HOAN_THIEN/histogram/liver_xoa_expand_needle/'
needle_folder = 'D:/SAN_PHAM_HOAN_THIEN/histogram/needle_expand_image/'

liver_histogram = 'D:/SAN_PHAM_HOAN_THIEN/histogram/histogram_needle_expand/liver/'
needle_histogram = 'D:/SAN_PHAM_HOAN_THIEN/histogram/histogram_needle_expand/needle/'
liver_needle_histogram = 'D:/SAN_PHAM_HOAN_THIEN/histogram/histogram_needle_expand/liver_needle/'
liver_and_needle_histogram = 'D:/SAN_PHAM_HOAN_THIEN/histogram/histogram_needle_expand/liver_and_needle/'
liver_and_liver_needle_histogram = 'D:/SAN_PHAM_HOAN_THIEN/histogram/histogram_needle_expand/liver_and_liver_needle/'



except_file = ['p014_inter_ar_006.nii.gz',
               'p014_inter_nc_002.nii.gz',
               'p014_inter_pv_007.nii.gz',
               'p017_inter_nc_002.nii.gz']
accept_file = ['p031_inter_pv_003.nii.gz']

for file in tqdm(os.listdir(needle_folder)):
    print("\nfile :", file)
    liver_needle_itk = sitk.ReadImage(os.path.join(liver_needle_folder, file))
    liver_itk = sitk.ReadImage(os.path.join(liver_folder, file))
    needle_itk = sitk.ReadImage(os.path.join(needle_folder, file))

    liver_needle_array = sitk.GetArrayFromImage(liver_needle_itk)
    liver_array = sitk.GetArrayFromImage(liver_itk)
    needle_array = sitk.GetArrayFromImage(needle_itk)

    # delete background
    ln_list = liver_needle_array.ravel()
    l_list = liver_array.ravel()
    n_list = needle_array.ravel()

    ln = [] # liver has needle label
    l = [] # liver deleded needle label
    n = [] # needle label
    # ln = liver_needle_array.ravel()
    # l = liver_array.ravel()
    # n = needle_array.ravel()
    """
    1 : plot ln and l
    2 3 4 : ln l n
    5 : plot ln l n 
    6 : l n
    """
    for i in range(1, len(ln_list)):
        if ln_list[i] != 0:
            ln.append(ln_list[i])
        if l_list[i] != 0:
            l.append(l_list[i])
        if n_list[i] != 0:
            n.append(n_list[i])

    histogram1, bin_edges1 = np.histogram(ln, bins=300, range=(-1000, 3000))
    histogram2, bin_edges2 = np.histogram(l, bins=300, range=(-1000, 3000))
    histogram3, bin_edges3 = np.histogram(n, bins=300, range=(-1000, 3000))

    ''' plot histogram '''

    # 1: plot ln and l

    fig1 = plt.figure(1)
    plt.title("Histogram")
    plt.xlabel("intensity")
    plt.ylabel("pixel count")
    plt.xlim([-1000, 3000])  # <- named arguments do not work here
    # ax3d.set_ylim([0, 1])
    plt.plot(bin_edges2[0:-1], histogram2, 'b')  # <- or here
    plt.legend(["Liver"], loc="upper right")
    fig1.show()
    plt.show()
    fig1.savefig(os.path.join(liver_histogram, file + '.png'), dpi=600)

    # plot ln
    fig2 = plt.figure(2)
    plt.title("Histogram")
    plt.xlabel("Intensity")
    plt.ylabel("Pixel Count")
    plt.xlim([-1000, 3000])  # <- named arguments do not work here
    # ax3d.set_ylim([0, 1])
    plt.plot(bin_edges3[0:-1], histogram3, 'b')  # <- or here
    plt.legend(["Needle"], loc="upper right")
    fig2.show()
    plt.show()
    fig2.savefig(os.path.join(needle_histogram, file + '.png'), dpi=600)

    # plot l
    fig3 = plt.figure(3)
    plt.title("Histogram")
    plt.xlabel("Intensity")
    plt.ylabel("Pixel Count")
    plt.xlim([-1000, 3000])  # <- named arguments do not work here
    # ax3d.set_ylim([0, 1])
    plt.plot(bin_edges2[0:-1], histogram2, 'b')  # <- or here
    plt.plot(bin_edges3[0:-1], histogram3, 'r')
    plt.legend(["Liver","Needle"], loc="upper right")
    fig3.show()
    plt.show()
    fig3.savefig(os.path.join(liver_and_needle_histogram, file + '.png'), dpi=600)

    # plot n
    fig4 = plt.figure(4)
    plt.title("Histogram")
    plt.xlabel("Intensity")
    plt.ylabel("Pixel Count")
    plt.xlim([-1000, 3000])  # <- named arguments do not work here
    # ax3d.set_ylim([0, 1])
    plt.plot(bin_edges1[0:-1], histogram1, 'b')
    plt.plot(bin_edges2[0:-1], histogram2, 'r')
    plt.legend(["Liver","Liver and Needle"], loc="upper right")
    fig4.show()
    plt.show()
    fig4.savefig(os.path.join(liver_and_liver_needle_histogram, file + '.png'), dpi=600)

    # plot n
    fig5 = plt.figure(5)
    plt.title("Histogram")
    plt.xlabel("Intensity")
    plt.ylabel("Pixel Count")
    plt.xlim([-1000, 3000])  # <- named arguments do not work here
    # ax3d.set_ylim([0, 1])
    plt.plot(bin_edges1[0:-1], histogram1, 'b')
    plt.legend(["Liver and Needle"], loc="upper right")
    fig5.show()
    plt.show()
    fig5.savefig(os.path.join(liver_needle_histogram, file + '.png'), dpi=600)