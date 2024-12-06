import h5py
import numpy as np
from skimage.morphology import skeletonize
from scipy.spatial import distance_matrix
from pathlib import Path
import os
import json
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from scipy import interpolate


def load_img(path,bounds):
    print('bounds')
    try:
        bounds = np.array(bounds.split(' ')).astype(float).astype(int)
    except:
        print('except')
    #     bounds = np.array(bounds.split(' '))

    with h5py.File(path,'r') as f:
        img = np.zeros((bounds[1]-bounds[0],bounds[3]-bounds[2]))
        f['Image'].read_direct(img,(slice(bounds[0],bounds[1]),slice(bounds[2],bounds[3])))
    return img


def create_mask(viewer):
    top_layer = viewer.layers[-1]
    if type(top_layer).__name__ == "Shapes":
        mask = top_layer.to_labels(labels_shape=viewer.layers[0].data.shape[0:2])

        skelleton = skeletonize(mask)
        viewer.add_image(
            skelleton, colormap="green", blending="translucent", opacity=0.5
        )
        for i in viewer.layers:
            if i.name == "Shapes":
                viewer.layers.remove(i)

def export_mask_points(viewer,bounds):
    mask_points, start_point, end_point = sort_mask_points(viewer.layers[-1].data)
    res_path = Path(os.getcwd()) / 'programme/viewer_napari/results/preused_masks/mask_0.json'
    num = 0
    while os.path.exists(res_path):
        res_path = Path(os.getcwd()) / f'programme/viewer_napari/results/preused_masks/mask_{num}.json'
        num+=1
    mask_res = {'mask_points':mask_points.tolist(),
                'start_point':start_point,
                'end_point':end_point,
                'bounds':bounds}
    with open(res_path,'w') as f:
        json.dump(mask_res,f)






def sort_mask_points(mask):
    mask_cords = []
    for a in range(len(mask)):
        for b in range(len(mask[0])):
            if mask[a,b] ==1:
                mask_cords.append([a,b])
    dist_mat = distance_matrix(mask_cords,mask_cords)
    canidates = np.where((dist_mat > 0) & (dist_mat <= np.sqrt(2)), 1, 0)
    start_points = np.where(canidates.sum(axis=1) == 1)
    start_point = start_points[0][1]
    end_point = start_points[0][0]

    mask_sorted = [mask_cords[start_point]]

    running_point = start_point
    last_point = start_point
    while running_point != end_point:

        last_point1 = running_point
        running_point = np.array(np.where(canidates[running_point] == 1))[0]

        running_point = running_point[0 if running_point[0] != last_point else 1]
        mask_sorted.append(mask_cords[running_point])
        last_point = last_point1
    return np.array(mask_sorted).T, mask_cords[start_point], mask_cords[end_point]
  

def get_angles(mask_points):
    angles = []
    last_angle = 0
    mask_points = np.array(mask_points).T
    for i in range(len(mask_points)-1):
        point_in = mask_points[i]
        point_n = mask_points[i+1]

        vec = point_n-point_in
        angle = np.arctan2(vec[1],vec[0])
        angle = (np.degrees(angle)+90) % 180
        if angle == 0 and last_angle > 90:
            angle = 180
        elif angle == 0 and last_angle<=90:
            angle = 0
        angles.append(angle)
        last_angle = angle
    return angles


def remap_180(data):
    data = np.array(data)
    dat_new = np.zeros(len(data)//2)
    if len(data) == 360:
      
        dat_new[0:90] = data[90:180]+data[270:360]
        dat_new[90:180] = data[0:90]+ data[180:270]
        return dat_new
    else:
        raise ValueError("Data not 360")



def plot_config(plot_font_size=12):
    plt.legend(fontsize=plot_font_size)
    plt.grid(color='grey', linestyle='--', linewidth=0.7)
    plt.ylabel("Häufigkeit",fontsize=plot_font_size)
    plt.xlabel("Differenz in °",fontsize=plot_font_size)
    plt.xticks(fontsize=plot_font_size)
    plt.yticks(fontsize=plot_font_size)
    plt.gcf().subplots_adjust(left=0.15)
    plt.gcf().subplots_adjust(bottom=0.15)


def min_diff_interp(dat1, dat2):
    if True:
        dat2 = gaussian_filter(np.array(dat2), sigma=3)
        dat2_new = interpolate_dat(np.arange(len(dat2)),dat2,np.arange(-0.5,len(dat2)+0.5))
        if len(dat1) == len(dat2_new):
            diff = np.array(dat1) - np.array(dat2_new)
            return diff
        else:
            print('shapes dont match')


def interpolate_dat(data_x,data_y,reference):
    interpolated_dat = interpolate.interp1d(
            data_x,data_y, kind="cubic", fill_value="extrapolate"
        )
    return interpolated_dat(reference)

