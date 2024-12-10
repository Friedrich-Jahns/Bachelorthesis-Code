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



def plot_config(plot_font_size=12,param='direction'):
    plt.legend(fontsize=plot_font_size)
    plt.grid(color='grey', linestyle='--', linewidth=0.7)
    if param == 'direction':
        plt.xlabel("Differenz in °",fontsize=plot_font_size)
        plt.ylabel("Häufigkeit",fontsize=plot_font_size)
    if param == 'inclination':
        plt.xlabel("Inklination in °",fontsize=plot_font_size)
        plt.ylabel("Häufigkeit",fontsize=plot_font_size)
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

def load_pre_used_line_mask(viewer,mask_no):
    try:
        mask_no_list = [int(mask_no)]
    except:
        try:
            mask_no_list = np.array(mask_no.split(",")).astype(int)
        except:
            bounds = np.array(mask_no.split(":")).astype(int)
            mask_no_list = np.arange(*bounds)
    print(mask_no_list)
    
    mask_in = np.zeros((viewer.layers[0].data.shape[0:2]))
    with open(Path(os.getcwd()) / 'programme/viewer_napari/layers_info.json') as f:
        bounds_image = json.load(f)['bounds']
    for mask_nr in mask_no_list:
        with open(Path(os.getcwd()) / f'programme/viewer_napari/results/preused_masks/mask_{mask_nr}.json') as f:
            dat = json.load(f)
        if dat['bounds'] != bounds_image:
            print(f"Bounds do not match! Mask generatet on bounds {bounds}")
            return
        for points in np.array(dat['mask_points']).T:
            points = points.astype(int)
            mask_in[points[0],points[1]] = 1
    viewer.add_image(mask_in, blending="additive", colormap="green", name="skelleton")


def get_shape(path):
    with h5py.File(path,'r') as f:
        return f['Image'].shape

def diff_mask(viewer,paths,threshold):
    box_size = 256
    res_path = Path(os.getcwd()) / 'programme/viewer_napari/results/diff_masks'
    full_path = res_path/f"Threshold_{threshold}-{box_size}-{paths[0].stem}-{paths[1].stem}.txt"
    if full_path.exists():
        print('file already exists')
    else:
        f = open(full_path,'w')
        try:
            if threshold.split('_')[-1] == 'abs':
                absoulute = True
                thresh = int(threshold.split('_')[0])
        except:
            absoulute = False
            thresh = int(threshold)
        print(f'thresh:{threshold}')

        if get_shape(paths[0])==get_shape(paths[1]):
            shape = get_shape(paths[0])
        else:
            print('shapes do no match')
            exit()

        y_iterations = shape[0] // box_size
        y_rest = shape[0] % box_size
        x_iterations = shape[1] // box_size
        x_rest = shape[1] % box_size\
        
        for a in range(y_iterations):
            for b in range(x_iterations):
                start = [a*box_size,b*box_size]
                size = [box_size,box_size]
                if a >= y_iterations:
                    size[0] = y_rest
                if b >= x_iterations:
                    size[1] = x_rest
                
                box_bounds = f'{start[0]} {start[0]+size[0]} {start[1]} {start[1]+size[1]}'

                img1 = load_img(paths[0],box_bounds)
                img2 = load_img(paths[1],box_bounds)
                print(f"\r{start} / {shape}", end="")    

                if absoulute:
                    img1 = np.abs(img1)
                    img2 = np.abs(img2)
                threshed = np.abs(img1-img2) > thresh
                rel_thresed = np.sum(threshed.astype(int)) / np.prod(threshed.shape)
                f.write(
                    str(start[0])
                    + "\t"
                    + str(start[0] + size[0])
                    + "\t"
                    + str(start[1])
                    + "\t"
                    + str(start[1] + size[1])
                    + "\t"
                    + str(rel_thresed)
                    + "\n"
                )
                del img1,img2
        f.close()
    return full_path

def load_diff_mask(viewer,path):
    with open(path,'r') as f:
        data = np.loadtxt(f,delimiter='\t')
    viewer.add_image(plot_rois(data), colormap="PiYG")


def plot_rois(roi):
    arr = np.empty(
        (int(max(roi.T[1])) // 100, int(max(roi.T[3])) // 100)
    )
    for i in range(len(roi)):
        arr[
            int(roi[i, 0]) // 100 : int(roi[i, 1]) // 100,
            int(roi[i, 2]) // 100 : int(roi[i, 3]) // 100,
        ] = (
            roi[i, 4] if roi[i, 4] != float(1) else 0
        )
    return arr


def straight_line_prof(img,mask):
    img = np.array(img)
    mask_arr = np.zeros((img.shape))
    mask_points = np.array(mask).T
    for i in mask_points:
        mask_arr[i[0],i[1]] = 1
    masked_image = mask_arr*img
    profile1 = np.trim_zeros(masked_image.sum(0))
    profile2 = np.trim_zeros(masked_image.T.sum(0))
    return [profile1 if len(profile1)>len(profile2) else profile2]

def example_angled_straight_line():
    img = np.zeros((100,100))
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i,j] = agled_straight_line_func(i,j)
    return img

def agled_straight_line_func(x,y):
    if x>5 and y>5 and x<95 and y<95 and np.abs(x-(.6*y))<.5:
        return 1      
    else:
        return 0
    
def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')