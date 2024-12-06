import os
from pathlib import Path
import json
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import lmfit
import numpy as np
from scipy import interpolate
import sys
sys.path.append(str(Path(os.getcwd()) / 'programme/viewer_napari/lib'))
import func




path = Path(os.getcwd()) / "programme/analysis/diretion/profiles"
data = []
files = os.listdir(path)
files_sorted = sorted(files,key = lambda x:int(x.split('_')[-1].split('.')[0]))

for file in files_sorted:
    with open(path / file,'r') as f:
        dat = json.load(f)
        data.append(dat)

turn = []
with open(Path(os.getcwd()) / 'programme/analysis/diretion/turn.csv','r') as f:
    for l in f:
        dat = l.strip().split(';')
        dat[0] = int(dat[0])
        turn.append(dat)
    turn = dict(turn)



number = {"LMP1": (63-63, 163-63), "LMP3D-D": (163-63, 234-63), "LMP3D-R": (234-63, 313-63)}



for source, num in number.items():
    von, bis = num
    
    res_path = Path(os.getcwd()) / f'programme/analysis/diretion/results/{source}'
    if os.path.exists(res_path) != True:
        os.makedirs(res_path)
    for i in range(3):
        print()
    print(f'============={source}============')

    count = [0,0,0]
    length = [0,0,0]

    for i in data[von:bis]:
        diff = func.min_diff_interp(i[source][0], i["angle"])

        if turn[i['mask_nr']] == "r":
            length[0]=length[0]+len(diff)
            count[0]=count[0]+1
        elif turn[i['mask_nr']] == "l":
            length[1]=length[1]+len(diff)
            count[1]=count[1]+1
        elif turn[i['mask_nr']] == "m":
            length[2]=length[2]+len(diff)
            count[2]=count[2]+1

    corr_turn_r = 1/(length[0]/np.sum(length))
    corr_turn_l = 1/(length[1]/np.sum(length))
    corr_turn_m = 1/(length[2]/np.sum(length))
    print(corr_turn_r)