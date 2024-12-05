from gui.load_images_gui import *
from PySide6 import QtCore, QtGui, QtWidgets
import os
import subprocess
from pathlib import Path
import json

viewer = os.getcwd() + "/programme/viewer_napari/main.py"
miniconda_dir = "/home/friedrichjahns/miniconda3/envs/bsc_conda/bin/python"

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoadImages()
        self.ui.setupUi(self)

        try:
            with open(Path(os.getcwd()) / 'programme/viewer_napari/layers_info.json','r') as f:
                preset = json.load(f)
                bounds_pre = preset['bounds'].split(' ')
                self.ui.lineEdit_2.setText(str(bounds_pre[0]))
                self.ui.lineEdit_3.setText(str(bounds_pre[1]))
                self.ui.lineEdit_4.setText(str(bounds_pre[2]))
                self.ui.lineEdit_5.setText(str(bounds_pre[3]))
                dat_path_pre = preset['data_path']
                res_path_pre = preset['result_path']
                thresh_pre = preset['thresh']


        except:
            print('no preset exists')



        def load_files():
            path = lambda: self.ui.lineEdit.text()
            files = os.listdir(path())
            for i in files:
                self.ui.listWidget.addItem(i)
 
        try:
            load_files()
        except:
            print('No Path given')

        self.ui.listWidget.setSelectionMode(QListWidget.MultiSelection)

        items = lambda: [item.text() for item in self.ui.listWidget.selectedItems()]
        dat_path = lambda: self.ui.lineEdit.text()
        res_path = lambda: self.ui.lineEdit_6.text()
        bounds = (
            lambda: f"{int(self.ui.lineEdit_2.text())} {int(self.ui.lineEdit_3.text())} {int(self.ui.lineEdit_4.text())} {int(self.ui.lineEdit_5.text())}"
        )
        thresh = lambda: self.ui.lineEdit_7.text()

        def start_napari():
            cwd = Path(os.getcwd())
            dat = {'files':items(),'data_path':dat_path(),'result_path':res_path(),'bounds':bounds(),'threshold':thresh()}
            with open( cwd / 'programme/viewer_napari/layers_info.json','w') as f:
                json.dump(dat,f)

            subprocess.run([miniconda_dir,viewer],cwd = os.getcwd())


        #Buttons
        self.ui.pushButton.clicked.connect(lambda: load_files())
        self.ui.buttonBox.rejected.connect(self.close)
        self.ui.buttonBox.accepted.connect(lambda:start_napari())

        


        



if __name__ == "__main__":

    import sys

    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
