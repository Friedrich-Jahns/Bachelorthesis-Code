import napari
import sys
from pathlib import Path
import h5py
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget
import numpy as np
import sys
import lib.func as func
import matplotlib.pyplot as plt
import json
import os


viewer = napari.Viewer()


# Buttons

layout1 = QVBoxLayout()

create_mask = QPushButton('Create Mask')
create_mask.clicked.connect(lambda:func.create_mask(viewer))
layout1.addWidget(create_mask)

export_mask_points = QPushButton('Export Maskpoints')
export_mask_points.clicked.connect(lambda:func.export_mask_points(viewer,load_info['bounds']))
layout1.addWidget(export_mask_points)

widget = QWidget()
widget.setLayout(layout1)
viewer.window.add_dock_widget(widget, area="left")




with open(Path(os.getcwd()) / 'programme/viewer_napari/layers_info.json','r') as f:
    load_info = json.load(f)
paths = []
for i in load_info['files']:
    paths.append(Path(load_info['data_path']) / i)
for path in paths:
    layer = viewer.add_image(func.load_img(path,load_info['bounds']))
    layer.name = path.stem
napari.run()