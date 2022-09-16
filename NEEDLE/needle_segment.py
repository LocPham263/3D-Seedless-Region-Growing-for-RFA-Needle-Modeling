import numpy as np
import SimpleITK as sitk

def grow(img, seed, t):
    """
    img: ndarray, ndim=3
        An image volume.
    
    seed: tuple, len=3
        Region growing starts from this point.

    t: int
        The image neighborhood radius for the inclusion criteria.
    """
    seg = np.zeros(img.shape, dtype=np.bool)
    checked = np.zeros_like(seg)

    seg[seed] = True
    checked[seed] = True
    needs_check = get_nbhd(seed, checked, img.shape)

    while len(needs_check) > 0:
        pt = needs_check.pop()

        # Its possible that the point was already checked and was
        # put in the needs_check stack multiple times.
        if checked[pt]: continue

        checked[pt] = True

        # Handle borders.
        imin = max(pt[0]-t, 0)
        imax = min(pt[0]+t, img.shape[0]-1)
        jmin = max(pt[1]-t, 0)
        jmax = min(pt[1]+t, img.shape[1]-1)
        kmin = max(pt[2]-t, 0)
        kmax = min(pt[2]+t, img.shape[2]-1)

        if img[pt] >= img[imin:imax+1, jmin:jmax+1, kmin:kmax+1].mean():
            # Include the voxel in the segmentation and
            # add its neighbors to be checked.
            seg[pt] = True
            needs_check += get_nbhd(pt, checked, img.shape)

    return seg

def get_nbhd(pt, checked, dims):
    nbhd = []

    if (pt[0] > 0) and not checked[pt[0]-1, pt[1], pt[2]]:
        nbhd.append((pt[0]-1, pt[1], pt[2]))
    if (pt[1] > 0) and not checked[pt[0], pt[1]-1, pt[2]]:
        nbhd.append((pt[0], pt[1]-1, pt[2]))
    if (pt[2] > 0) and not checked[pt[0], pt[1], pt[2]-1]:
        nbhd.append((pt[0], pt[1], pt[2]-1))

    if (pt[0] < dims[0]-1) and not checked[pt[0]+1, pt[1], pt[2]]:
        nbhd.append((pt[0]+1, pt[1], pt[2]))
    if (pt[1] < dims[1]-1) and not checked[pt[0], pt[1]+1, pt[2]]:
        nbhd.append((pt[0], pt[1]+1, pt[2]))
    if (pt[2] < dims[2]-1) and not checked[pt[0], pt[1], pt[2]+1]:
        nbhd.append((pt[0], pt[1], pt[2]+1))

    return nbhd

def get_idx(ct):
    s,x,y = ct.shape
    max_idx = ct.argmax()
    cur_slice = np.int(max_idx / (x*y))
    sub_idx = max_idx - cur_slice*x*y
    x_idx = np.int(sub_idx/x)
    y_idx = sub_idx - x_idx * x

    idx = (cur_slice, x_idx, y_idx)
    return idx
    
def needle_segment(ct_array, liver_array, thresh):
    mask = ct_array * liver_array

    idx = get_idx(mask) # lấy tọa độ điểm max

    if mask[idx[0], idx[1], idx[2]] < 300: # trường hợp liver segment sai (điểm chọn ko thuộc vùng gan)
        idx = get_idx(ct_array) # chọn lại điểm max cho cả file ảnh CT

    ct_array[ct_array < thresh] = 0 # dựa vào ngưỡng để tạo nhãn : 500 là thresh tối ưu
    ct_array[ct_array >= thresh] = 1

    ct_array = grow(ct_array, (idx[0], idx[1], idx[2]), 5).astype(np.int16) # từ đó thực hiện thuật toán region growing

    seg_sitk = sitk.GetImageFromArray(ct_array)

    return ct_array, seg_sitk

