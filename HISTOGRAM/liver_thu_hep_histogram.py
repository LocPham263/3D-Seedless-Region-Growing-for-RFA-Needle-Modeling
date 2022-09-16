import os
import shutil
import numpy as np
import SimpleITK as sitk

import matplotlib.pyplot as plt
from tqdm import tqdm

liver_needle_folder = 'D:/SAN_PHAM_HOAN_THIEN/histogram/thu_hep_liver_histogram/mask/liver_needle_mask/'
liver_folder = 'D:/SAN_PHAM_HOAN_THIEN/histogram/thu_hep_liver_histogram/mask/liver_mask/'
needle_folder = 'D:/SAN_PHAM_HOAN_THIEN/histogram/thu_hep_liver_histogram/mask/needle_mask/'

liver_histogram = 'D:/SAN_PHAM_HOAN_THIEN/histogram/thu_hep_liver_histogram/histogram/liver/'
needle_histogram = 'D:/SAN_PHAM_HOAN_THIEN/histogram/thu_hep_liver_histogram/histogram/needle/'
liver_needle_histogram = 'D:/SAN_PHAM_HOAN_THIEN/histogram/thu_hep_liver_histogram/histogram/liver_needle/'
liver_and_needle_histogram = 'D:/SAN_PHAM_HOAN_THIEN/histogram/thu_hep_liver_histogram/histogram/liver_and_needle/'
liver_and_liver_needle_histogram = 'D:/SAN_PHAM_HOAN_THIEN/histogram/thu_hep_liver_histogram/histogram/liver_and_liver_needle/'

except_file = []
accept_file = []

for file in tqdm(os.listdir(needle_folder)):
    print("\nfile :", file)
    liver_needle_itk = sitk.ReadImage(os.path.join(liver_needle_folder, file))
    liver_itk = sitk.ReadImage(os.path.join(liver_folder, file))
    needle_itk = sitk.ReadImage(os.path.join(needle_folder, file))

    liver_needle_array = sitk.GetArrayFromImage(liver_needle_itk)
    liver_array = sitk.GetArrayFromImage(liver_itk)
    needle_array = sitk.GetArrayFromImage(needle_itk)

    ln = liver_needle_array.ravel()
    l = liver_array.ravel()
    n = needle_array.ravel()
    # delete background
    # ln_list = liver_needle_array.ravel()
    # l_list = liver_array.ravel()
    # n_list = needle_array.ravel()
    #
    # ln = [] # liver has needle label
    # l = [] # liver deleded needle label
    # n = [] # needle label

    """
    1 : plot ln and l
    2 3 4 : ln l n
    5 : plot ln l n 
    6 : l n
    """
    # for i in range(1, len(ln_list)):
    #     if ln_list[i] != 0:
    #         ln.append(ln_list[i])
    #     if l_list[i] != 0:
    #         l.append(l_list[i])
    #     if n_list[i] != 0:
    #         n.append(n_list[i])

    histogram1, bin_edges1 = np.histogram(ln, bins=300, range=(-1000, 3000))
    histogram2, bin_edges2 = np.histogram(l, bins=300, range=(-1000, 3000))
    histogram3, bin_edges3 = np.histogram(n, bins=300, range=(-1000, 3000))

    ''' plot histogram '''

    # 1: plot ln and l

    # plot l
    fig3 = plt.figure(3)
    plt.title("Histogram", fontsize=18)
    plt.xlabel("Intensity", fontsize=18)
    plt.ylabel("Pixel Count", fontsize=18)
    plt.xlim([-1000, 3000])  # <- named arguments do not work here
    # ax3d.set_ylim([0, 1])
    plt.plot(bin_edges2[0:-1], histogram2, 'b')  # <- or here
    plt.plot(bin_edges3[0:-1], histogram3, 'r')
    plt.plot([0,500], 'g')
    plt.legend(["Liver","Needle"], loc="upper right", fontsize=18)
    fig3.show()

    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)

    plt.show()
    # fig3.savefig(os.path.join(liver_and_needle_histogram, file + '300.png'), dpi=600)

    # fig1 = plt.figure(1)
    # plt.title("Histogram", fontsize=18)
    # plt.xlabel("intensity", fontsize=18)
    # plt.ylabel("pixel count", fontsize=18)
    # plt.xlim([-1000, 3000])  # <- named arguments do not work here
    # # ax3d.set_ylim([0, 1])
    # plt.plot(bin_edges2[0:-1], histogram2, 'b')  # <- or here
    # plt.legend(["Liver"], loc="upper right")
    # fig1.show()
    # plt.show()
    # fig1.savefig(os.path.join(liver_histogram, file + '300.png'), dpi=600)
    #
    # # plot ln
    # fig2 = plt.figure(2)
    # plt.title("Histogram")
    # plt.xlabel("Intensity")
    # plt.ylabel("Pixel Count")
    # plt.xlim([-1000, 3000])  # <- named arguments do not work here
    # # ax3d.set_ylim([0, 1])
    # plt.plot(bin_edges3[0:-1], histogram3, 'b')  # <- or here
    # plt.legend(["Needle"], loc="upper right")
    # fig2.show()
    # plt.show()
    # fig2.savefig(os.path.join(needle_histogram, file + '300.png'), dpi=600)
    #
    #
    # # plot n
    # fig4 = plt.figure(4)
    # plt.title("Histogram")
    # plt.xlabel("Intensity")
    # plt.ylabel("Pixel Count")
    # plt.xlim([-1000, 3000])  # <- named arguments do not work here
    # # ax3d.set_ylim([0, 1])
    # plt.plot(bin_edges1[0:-1], histogram1, 'b')
    # plt.plot(bin_edges2[0:-1], histogram2, 'r')
    # plt.legend(["Liver and Needle","Liver"], loc="upper right")
    # fig4.show()
    # plt.show()
    # fig4.savefig(os.path.join(liver_and_liver_needle_histogram, file + '300.png'), dpi=600)
    #
    # # plot n
    # fig5 = plt.figure(5)
    # plt.title("Histogram")
    # plt.xlabel("Intensity")
    # plt.ylabel("Pixel Count")
    # plt.xlim([-1000, 3000])  # <- named arguments do not work here
    # # ax3d.set_ylim([0, 1])
    # plt.plot(bin_edges1[0:-1], histogram1, 'b')
    # plt.legend(["Liver and Needle"], loc="upper right")
    # fig5.show()
    # plt.show()
    # fig5.savefig(os.path.join(liver_needle_histogram, file + '300.png'), dpi=600)