import os
from pathlib import Path
import json
import matplotlib.pyplot as plt
import lmfit
import numpy as np
from scipy import interpolate
import sys
sys.path.append(str(Path(os.getcwd()) / 'programme/viewer_napari/lib'))
import func




path = Path(os.getcwd()) / "programme/analysis/inklination/profiles"
data = []
files = os.listdir(path)
files_sorted = sorted(files,key = lambda x:int(x.split('_')[-1].split('.')[0]))

for file in files_sorted:
    with open(path / file,'r') as f:
        dat = json.load(f)
        data.append(dat)



number = {"LMP1": (63-63, 163-63), "LMP3D-D": (163-63, 234-63), "LMP3D-R": (234-63, 313-63)}



for source, num in number.items():
    von, bis = num
    
    res_path = Path(os.getcwd()) / f'programme/analysis/inklination/results/{source}'
    if os.path.exists(res_path) != True:
        os.makedirs(res_path)
    for i in range(3):
        print()
    print(f'============={source}============')

    hist = []
    for i in data[von:bis]:
        hist = np.concatenate((hist,i[source]))

   
    
    counts,x_edges = np.histogram(hist,bins=180)
    counts = counts + 0.1

    lmfit_model = lmfit.models.GaussianModel()
    params = lmfit_model.guess(counts, x=np.arange(-90,90))
    result = lmfit_model.fit(counts, params, x=np.arange(-90,90), weights=1 / np.sqrt(counts),nan_policy='propagate')
    
    plt.plot(np.arange(-90,90), result.best_fit, color="red",label=f'Bester Fit')
    plt.bar(range(-90,90),counts, color='steelblue',width=1,label=f"Daten")
    func.plot_config()
    plt.savefig(res_path / f"{source}_histogram.png")
    plt.clf()
    with open(res_path/'fit_report.txt','w') as f:
        f.write(result.fit_report())

    counts,x_edges = np.histogram(np.abs(hist),bins=90)
    counts = counts + 0.1

    lmfit_model = lmfit.models.GaussianModel()
    params = lmfit_model.guess(counts, x=np.arange(0,90))
    result = lmfit_model.fit(counts, params, x=np.arange(0,90), weights=1 / np.sqrt(counts),nan_policy='propagate')
    
    plt.plot(np.arange(0,90), result.best_fit, color="red",label=f'Bester Fit')
    plt.bar(range(0,90),counts, color='steelblue',width=1,label=f"Daten")
    func.plot_config()
    plt.savefig(res_path / f"{source}_histogram_abs.png")
    plt.clf()
    with open(res_path/'fit_report_abs.txt','w') as f:
        f.write(result.fit_report())