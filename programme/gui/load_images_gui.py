# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'load_images_guiiQYMyP.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFrame, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QWidget)

class Ui_LoadImages(object):
    def setupUi(self, LoadImages):
        if not LoadImages.objectName():
            LoadImages.setObjectName(u"LoadImages")
        LoadImages.resize(695, 388)
        self.buttonBox = QDialogButtonBox(LoadImages)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(440, 260, 201, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.lineEdit = QLineEdit(LoadImages)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(10, 40, 311, 25))
        self.label = QLabel(LoadImages)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 20, 54, 17))
        self.listWidget = QListWidget(LoadImages)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(10, 80, 311, 211))
        self.lineEdit_2 = QLineEdit(LoadImages)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(430, 70, 51, 25))
        self.label_2 = QLabel(LoadImages)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(400, 40, 191, 17))
        self.label_3 = QLabel(LoadImages)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(410, 70, 16, 17))
        self.label_4 = QLabel(LoadImages)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(410, 100, 16, 17))
        self.label_5 = QLabel(LoadImages)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(490, 70, 16, 17))
        self.lineEdit_3 = QLineEdit(LoadImages)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(500, 70, 51, 25))
        self.lineEdit_4 = QLineEdit(LoadImages)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setGeometry(QRect(430, 100, 51, 25))
        self.label_6 = QLabel(LoadImages)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(490, 100, 16, 17))
        self.lineEdit_5 = QLineEdit(LoadImages)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setGeometry(QRect(500, 100, 51, 25))
        self.pushButton = QPushButton(LoadImages)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(330, 40, 51, 25))
        self.line = QFrame(LoadImages)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(380, 40, 21, 241))
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_2 = QFrame(LoadImages)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(10, 310, 641, 16))
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.label_7 = QLabel(LoadImages)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 330, 301, 17))
        self.lineEdit_6 = QLineEdit(LoadImages)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setGeometry(QRect(10, 350, 311, 25))
        self.pushButton_2 = QPushButton(LoadImages)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(420, 350, 211, 25))
        self.line_3 = QFrame(LoadImages)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setGeometry(QRect(380, 330, 20, 51))
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)
        self.label_8 = QLabel(LoadImages)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(630, 330, 61, 17))
        self.lineEdit_7 = QLineEdit(LoadImages)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        self.lineEdit_7.setGeometry(QRect(642, 350, 41, 25))

        self.retranslateUi(LoadImages)
        # self.buttonBox.accepted.connect(LoadImages.accept)
        # self.buttonBox.rejected.connect(LoadImages.reject)

        QMetaObject.connectSlotsByName(LoadImages)
    # setupUi

    def retranslateUi(self, LoadImages):
        LoadImages.setWindowTitle(QCoreApplication.translate("LoadImages", u"Dialog", None))
        self.lineEdit.setText(QCoreApplication.translate("LoadImages", u"/path/to/folder/", None))
        self.label.setText(QCoreApplication.translate("LoadImages", u"File Path", None))
        self.lineEdit_2.setText(QCoreApplication.translate("LoadImages", u"0", None))
        self.label_2.setText(QCoreApplication.translate("LoadImages", u"Boundaries of Region of interest", None))
        self.label_3.setText(QCoreApplication.translate("LoadImages", u"x:", None))
        self.label_4.setText(QCoreApplication.translate("LoadImages", u"y:", None))
        self.label_5.setText(QCoreApplication.translate("LoadImages", u":", None))
        self.lineEdit_3.setText(QCoreApplication.translate("LoadImages", u"1", None))
        self.lineEdit_4.setText(QCoreApplication.translate("LoadImages", u"0", None))
        self.label_6.setText(QCoreApplication.translate("LoadImages", u":", None))
        self.lineEdit_5.setText(QCoreApplication.translate("LoadImages", u"1", None))
        self.pushButton.setText(QCoreApplication.translate("LoadImages", u"refresh", None))
        self.label_7.setText(QCoreApplication.translate("LoadImages", u"File path for downsampled Images", None))
        self.lineEdit_6.setText(QCoreApplication.translate("LoadImages", u"/path/to/folder/", None))
        self.pushButton_2.setText(QCoreApplication.translate("LoadImages", u"ROI analysis of selectet Images", None))
        self.label_8.setText(QCoreApplication.translate("LoadImages", u"Threshold", None))
    # retranslateUi

