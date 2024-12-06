import napari
import sys
from pathlib import Path
import h5py
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget,QLineEdit
import numpy as np
import sys
import lib.func as func
import matplotlib.pyplot as plt
import json
import os


def global_mask_no(load_number):
    global mask_no
    mask_no = load_number

viewer = napari.Viewer()


# Buttons

layout1 = QVBoxLayout()

create_mask = QPushButton('Create Mask')
create_mask.clicked.connect(lambda:func.create_mask(viewer))
layout1.addWidget(create_mask)

export_mask_points = QPushButton('Export Maskpoints')
export_mask_points.clicked.connect(lambda:func.export_mask_points(viewer,load_info['bounds']))
layout1.addWidget(export_mask_points)

load_masks = QLineEdit()
load_masks.setPlaceholderText("Input mask Number")
# load_masks.returnPressed.connect(self.return_pressed)
load_masks.textChanged.connect(lambda:global_mask_no(load_masks.text()))

layout1.addWidget(load_masks)


load_pre_used_line_mask = QPushButton('Load preused line mask')
load_pre_used_line_mask.clicked.connect(lambda:func.load_pre_used_line_mask(viewer,mask_no))
layout1.addWidget(load_pre_used_line_mask)

widget = QWidget()
widget.setLayout(layout1)
viewer.window.add_dock_widget(widget, area="left")




with open(Path(os.getcwd()) / 'programme/viewer_napari/layers_info.json','r') as f:
    load_info = json.load(f)
if load_info['diff_mask']!=True:
    paths = []
    for i in load_info['files']:
        paths.append(Path(load_info['data_path']) / i)
    for path in paths:
        layer = viewer.add_image(func.load_img(path,load_info['bounds']))
        layer.name = path.stem

if load_info['diff_mask']:
    if len(load_info['files']) != 2:
        print('mor or less than 2 files selected')
        exit()
    paths = []
    for i in load_info['files']:
        paths.append(Path(load_info['data_path']) / i)
    diff_mask_path = func.diff_mask(viewer,paths,load_info['threshold'])
    func.load_diff_mask(viewer,diff_mask_path)


napari.run()