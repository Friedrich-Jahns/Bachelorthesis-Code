from pathlib import Path
import os
import numpy as np
import json
import sys
sys.path.append(str(Path(os.getcwd()) / 'programme/viewer_napari/lib'))
import func
import matplotlib.pyplot as plt


paths_dir = {'LAP':Path("/run/media/friedrichjahns/Data/Registrierte_schnitte/PE-2021-00981-H_00_s0920_LAP_Direction_Registered_Flat_v000.h5"),
         'LMP1':Path("/run/media/friedrichjahns/Data/Registrierte_schnitte/PE-2021-00981-H_00_s0920_PM_Complete_Direction_Registered_Flat_v001.h5"),
         'LMP3D-D':Path("/run/media/friedrichjahns/Data/Registrierte_schnitte/PE-2021-00981-H_00_s0920_PM_Complete_Direction_Registered_Flat_v002.h5"),
         'LMP3D-R':Path("/run/media/friedrichjahns/Data/Registrierte_schnitte/PE-2021-00981-H_00_s0920_PM_Complete_Direction_Registered_Flat_v000.h5")}

mask_path = Path(os.getcwd()) / 'programme/viewer_napari/results/preused_masks/'
# /home/friedrichjahns/Bachelorthesis-Code/programme/viewer_napari/results/mask_1.json

#direction
dat_res = {}
for redo_nr in range(63,313):
    with open(mask_path / f'mask_{redo_nr}.json','r') as f:
        dat = json.load(f)
    
    mask_points = dat['mask_points']
    bounds = np.array(str(dat['bounds']).split(' ')).astype(int)
    padd = 10
    bounds_corr = [min(mask_points[0])-padd,max(mask_points[0])+padd,min(mask_points[1])-padd,max(mask_points[1])+padd]
    bounds_new = bounds_corr +np.array([bounds[0],bounds[0],bounds[2],bounds[2]])
    bounds_new_str = f'{bounds_new[0]} {bounds_new[1]} {bounds_new[2]} {bounds_new[3]}'

    mask_points_padded = np.array(mask_points).T+np.array([padd,padd])
    mask_points_new = mask_points_padded-np.array([min(mask_points[0]),min(mask_points[1])])
    # print(len(np.array(mask_points).T),len(mask_points_new))
    # input()
    for key, value in paths_dir.items():
        print(value.stem)
        img = func.load_img(value,bounds_new_str)
        # plt.imshow(img,cmap='gray')
        # plt.plot(mask_points_new.T[1],mask_points_new.T[0])
        # plt.show()
        lineprofile = []

        for cords in mask_points_new:
            cords = np.array(cords).astype(int)
            lineprofile.append(img[*cords])
        dat_res[str(key)] = [float(x) for x in lineprofile]
        dat_res['mask_nr'] = redo_nr
        dat_res['mask_points'] = mask_points
        dat_res['bounds'] = dat['bounds']
        dat_res['angle'] = func.get_angles(mask_points)
    # print(len(func.get_angles(mask_points)),len(dat_res[str(key)]))
    with open( Path(os.getcwd()) / f'programme/analysis/diretion/profiles/Direction_mask_{redo_nr}.json','w') as f:
        json.dump(dat_res,f)

#inclination

paths_inc = {'LAP':Path("/run/media/friedrichjahns/Data/Registrierte_schnitte/PE-2021-00981-H_00_s0920_LAP_Inclination_Registered_Flat_v000.h5"),
         'LMP1':Path("/run/media/friedrichjahns/Data/Registrierte_schnitte/PE-2021-00981-H_00_s0920_PM_Complete_Direction_Registered_Flat_v002.h5"),
         'LMP3D-D':Path("/run/media/friedrichjahns/Data/Registrierte_schnitte/PE-2021-00981-H_00_s0920_PM_Complete_Direction_Registered_Flat_v001.h5"),
         'LMP3D-R':Path("/run/media/friedrichjahns/Data/Registrierte_schnitte/PE-2021-00981-H_00_s0920_PM_Complete_Direction_Registered_Flat_v000.h5")}

mask_path = Path(os.getcwd()) / 'programme/viewer_napari/results/preused_masks/'


dat_res = {}
for redo_nr in range(63,313):
    with open(mask_path / f'mask_{redo_nr}.json','r') as f:
        dat = json.load(f)
    mask_points = dat['mask_points']
    bounds = np.array(str(dat['bounds']).split(' ')).astype(int)
    padd = 10
    bounds_corr = [min(mask_points[0])-padd,max(mask_points[0])+padd,min(mask_points[1])-padd,max(mask_points[1])+padd]
    bounds_new = bounds_corr +np.array([bounds[0],bounds[0],bounds[2],bounds[2]])
    bounds_new_str = f'{bounds_new[0]} {bounds_new[1]} {bounds_new[2]} {bounds_new[3]}'

    mask_points_padded = np.array(mask_points).T+np.array([padd,padd])
    mask_points_new = mask_points_padded-np.array([min(mask_points[0]),min(mask_points[1])])
    
    lineprofile = []
    for key, value in paths_inc.items():
        print(value.stem)
        img = func.load_img(value,bounds_new_str)
        # plt.imshow(img,cmap='gray')
        # plt.plot(mask_points_new.T[1],mask_points_new.T[0])
        # plt.show()
        for cords in mask_points_new:
            cords = np.array(cords).astype(int)
            lineprofile.append(img[*cords])
        dat_res[str(key)] = [float(x) for x in lineprofile]
        dat_res['mask_nr'] = redo_nr
        dat_res['mask_points'] = mask_points
        dat_res['bounds'] = dat['bounds']
        dat_res['angle'] = func.get_angles(mask_points)
    with open( Path(os.getcwd()) / f'programme/analysis/inklination/profiles/Inclination_mask_{redo_nr}.json','w') as f:
        json.dump(dat_res,f)
