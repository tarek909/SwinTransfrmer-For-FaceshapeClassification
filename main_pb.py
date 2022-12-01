#global imports
from PyQt5.QtWidgets import QMainWindow,QApplication, QLabel, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QGridLayout, QMenuBar, QMenu
from PyQt5.QtGui import QPixmap
import sys
import cv2
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import pandas as pd
from PIL import Image
from tqdm.auto import tqdm
from sklearn.model_selection import train_test_split
import numpy as np
import torchvision.transforms as transforms
from torch.autograd import Variable
import torch
import torch.nn as nn
import torch.nn.functional as F
from datasets import load_dataset
import transformers
import time
from torch.utils.data import Dataset
from datasets import Dataset
from datasets import load_dataset, Image
from transformers import AutoFeatureExtractor
import torchvision.transforms.functional
from PIL import Image, ImageQt
import shutil
#local imports
from landmark_detection import Landmarks

from torchvision.transforms import (
    CenterCrop,
    Compose,
    Normalize,
    RandomHorizontalFlip,
    RandomResizedCrop,
    Resize,
    RandomAdjustSharpness,
    ToTensor

)

from datasets import load_metric
import numpy as np
from transformers import TrainingArguments, Trainer

from torch.utils.data import DataLoader
import torch
import qtawesome as qta


shapes =['Heart', 'Oblong', 'Oval', 'Round', 'Square']
model = torch.load('entire_model_final.pt', map_location=torch.device('cpu'))
feature_extractor = AutoFeatureExtractor.from_pretrained("microsoft/swin-tiny-patch4-window7-224")
normalize = Normalize(mean=feature_extractor.image_mean, std=feature_extractor.image_std)
_train_transforms = Compose(
        [
            Resize(feature_extractor.size),
            ToTensor(),
            normalize,
        ]
    )
def train_transforms(examples):
    examples['pixel_values'] = [_train_transforms(image.convert("RGB")) for image in examples['image']]
    return examples

def collate_fn(examples):
    pixel_values = torch.stack([example["pixel_values"] for example in examples])
    labels = torch.tensor([example["label"] for example in examples])
    return {"pixel_values": pixel_values, "labels": labels}


args = TrainingArguments(
    f"/",
    remove_unused_columns=False,
)

trainer = Trainer(
    model,
    args,
    data_collator=collate_fn,
)

landmarks_model=Landmarks()

#trainer initialization
img_init=np.zeros((1, 1, 3),dtype=np.uint8)
trainer_init=Dataset.from_dict({"image":[Image.fromarray(img_init)],"label":[0]})
trainer_init.set_transform(train_transforms)
trainer.predict(trainer_init)



class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
    def setPixmap(self, image):
        super().setPixmap(image)


class Ui_MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setupUi()

    def setupUi(self):
        self.resize(800, 600)
        self.setStyleSheet(
" background-color:#000000;\n"
"}\n"
"QDialog {\n"
"    background-color:#000000;\n"
"}\n"
"QColorDialog {\n"
"    background-color:#000000;\n"
"}\n"
"QTextEdit {\n"
"    background-color:#000000;\n"
"    color: #a9b7c6;\n"
"}\n"
"QPlainTextEdit {\n"
"    selection-background-color:#f39c12;\n"
"    background-color:#000000;\n"
"    border: 1px solid #FF00FF;\n"
"    color: #a9b7c6;\n"
"}\n"
"QPushButton{\n"
"    border: 1px transparent;\n"
"    color: #a9b7c6;\n"
"    padding: 2px;\n"
"    background-color: #000000;\n"
"}\n"
"QPushButton::default{\n"
"    border-style: solid;\n"
"    border-top-color: transparent;\n"
"    border-right-color: transparent;\n"
"    border-left-color: transparent;\n"
"    border-bottom-color: #e67e22;\n"
"    border-width: 1px;\n"
"    color: #a9b7c6;\n"
"    padding: 2px;\n"
"    background-color: #000000;\n"
"}\n"
"QPushButton:hover{\n"
"    border-style: solid;\n"
"    border-top-color: transparent;\n"
"    border-right-color: transparent;\n"
"    border-left-color: transparent;\n"
"    border-bottom-color: #FF00FF;\n"
"    border-bottom-width: 1px;\n"
"    border-style: solid;\n"
"    color: #FFFFFF;\n"
"    padding-bottom: 2px;\n"
"    background-color: #000000;\n"
"}\n"
"QPushButton:pressed{\n"
"    border-style: solid;\n"
"    border-top-color: transparent;\n"
"    border-right-color: transparent;\n"
"    border-left-color: transparent;\n"
"    border-bottom-color: #FF00FF;\n"
"    border-bottom-width: 2px;\n"
"    border-style: solid;\n"
"    color: #e67e22;\n"
"    padding-bottom: 1px;\n"
"    background-color: #000000;\n"
"}\n"
"QPushButton:disabled{\n"
"    border-style: solid;\n"
"    border-top-color: transparent;\n"
"    border-right-color: transparent;\n"
"    border-left-color: transparent;\n"
"    border-bottom-color: transparent;\n"
"    border-bottom-width: 2px;\n"
"    border-style: solid;\n"
"    color: #808086;\n"
"    padding-bottom: 1px;\n"
"    background-color: #000000;\n"
"}\n"
"QToolButton {\n"
"    border-style: solid;\n"
"    border-top-color: transparent;\n"
"    border-right-color: transparent;\n"
"    border-left-color: transparent;\n"
"    border-bottom-color: #e67e22;\n"
"    border-bottom-width: 1px;\n"
"    border-style: solid;\n"
"    color: #a9b7c6;\n"
"    padding: 2px;\n"
"    background-color: #000000;\n"
"}\n"
"QToolButton:hover{\n"
"    border-style: solid;\n"
"    border-top-color: transparent;\n"
"    border-right-color: transparent;\n"
"    border-left-color: transparent;\n"
"    border-bottom-color: #e67e22;\n"
"    border-bottom-width: 2px;\n"
"    border-style: solid;\n"
"    color: #FFFFFF;\n"
"    padding-bottom: 1px;\n"
"    background-color: #000000;\n"
"}\n"
"QLineEdit {\n"
"    border-width: 1px; border-radius: 4px;\n"
"    border-color: rgb(58, 58, 58);\n"
"    border-style: inset;\n"
"    padding: 0 8px;\n"
"    color: #a9b7c6;\n"
"    background:#000000;\n"
"    selection-background-color:#007b50;\n"
"    selection-color: #FFFFFF;\n"
"}\n"
"QLabel {\n"
"    color: #a9b7c6;\n"
"}\n"
"QLCDNumber {\n"
"    color: #e67e22;\n"
"}\n"
"QProgressBar {\n"
"    text-align: center;\n"
"    color: rgb(240, 240, 240);\n"
"    border-width: 1px; \n"
"    border-radius: 10px;\n"
"    border-color: rgb(58, 58, 58);\n"
"    border-style: inset;\n"
"    background-color:#000000;\n"
"}\n"
"QProgressBar::chunk {\n"
"    background-color: #e67e22;\n"
"    border-radius: 5px;\n"
"}\n"
"QMenu{\n"
"    background-color:#000000;\n"
"}\n"
"QMenuBar {\n"
"    background:rgb(0, 0, 0);\n"
"    color: #a9b7c6;\n"
"}\n"
"QMenuBar::item {\n"
"      spacing: 3px; \n"
"    padding: 1px 4px;\n"
"      background: transparent;\n"
"}\n"
"QMenuBar::item:selected { \n"
"      border-style: solid;\n"
"    border-top-color: transparent;\n"
"    border-right-color: transparent;\n"
"    border-left-color: transparent;\n"
"    border-bottom-color: #e67e22;\n"
"    border-bottom-width: 1px;\n"
"    border-style: solid;\n"
"    color: #FFFFFF;\n"
"    padding-bottom: 0px;\n"
"    background-color: #000000;\n"
"}\n"
"QMenu::item:selected {\n"
"    border-style: solid;\n"
"    border-top-color: transparent;\n"
"    border-right-color: transparent;\n"
"    border-left-color: #e67e22;\n"
"    border-bottom-color: transparent;\n"
"    border-left-width: 2px;\n"
"    color: #FFFFFF;\n"
"    padding-left:15px;\n"
"    padding-top:4px;\n"
"    padding-bottom:4px;\n"
"    padding-right:7px;\n"
"    background-color:#000000;\n"
"}\n"
"QMenu::item {\n"
"    border-style: solid;\n"
"    border-top-color: transparent;\n"
"    border-right-color: transparent;\n"
"    border-left-color: transparent;\n"
"    border-bottom-color: transparent;\n"
"    border-bottom-width: 1px;\n"
"    border-style: solid;\n"
"    color: #a9b7c6;\n"
"    padding-left:17px;\n"
"    padding-top:4px;\n"
"    padding-bottom:4px;\n"
"    padding-right:7px;\n"
"    background-color:#000000;\n"
"}\n"
"QTabWidget {\n"
"    color:rgb(0,0,0);\n"
"    background-color:#000000;\n"
"}\n"
"QTabWidget::pane {\n"
"        border-color: rgb(77,77,77);\n"
"        background-color:#000000;\n"
"        border-style: solid;\n"
"        border-width: 1px;\n"
"        border-radius: 6px;\n"
"}\n"
"QTabBar::tab {\n"
"    border-style: solid;\n"
"    border-top-color: transparent;\n"
"    border-right-color: transparent;\n"
"    border-left-color: transparent;\n"
"    border-bottom-color: transparent;\n"
"    border-bottom-width: 1px;\n"
"    border-style: solid;\n"
"    color: #808086;\n"
"    padding: 3px;\n"
"    margin-left:3px;\n"
"    background-color:#000000;\n"
"}\n"
"QTabBar::tab:selected, QTabBar::tab:last:selected, QTabBar::tab:hover {\n"
"      border-style: solid;\n"
"    border-top-color: transparent;\n"
"    border-right-color: transparent;\n"
"    border-left-color: transparent;\n"
"    border-bottom-color: #e67e22;\n"
"    border-bottom-width: 2px;\n"
"    border-style: solid;\n"
"    color: #FFFFFF;\n"
"    padding-left: 3px;\n"
"    padding-bottom: 2px;\n"
"    margin-left:3px;\n"
"    background-color:#000000;\n"
"}\n"
"\n"
"QCheckBox {\n"
"    color: #a9b7c6;\n"
"    padding: 2px;\n"
"}\n"
"QCheckBox:disabled {\n"
"    color: #808086;\n"
"    padding: 2px;\n"
"}\n"
"\n"
"QCheckBox:hover {\n"
"    border-radius:4px;\n"
"    border-style:solid;\n"
"    padding-left: 1px;\n"
"    padding-right: 1px;\n"
"    padding-bottom: 1px;\n"
"    padding-top: 1px;\n"
"    border-width:1px;\n"
"    border-color: rgb(87, 97, 106);\n"
"    background-color:#000000;\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    border-style:solid;\n"
"    border-width: 1px;\n"
"    border-color: #e67e22;\n"
"    color: #a9b7c6;\n"
"    background-color: #e67e22;\n"
"}\n"
"QCheckBox::indicator:unchecked {\n"
"\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    border-style:solid;\n"
"    border-width: 1px;\n"
"    border-color: #e67e22;\n"
"    color: #a9b7c6;\n"
"    background-color: transparent;\n"
"}\n"
"QRadioButton {\n"
"    color: #a9b7c6;\n"
"    background-color:#000000;\n"
"    padding: 1px;\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    border-style:solid;\n"
"    border-radius:5px;\n"
"    border-width: 1px;\n"
"    border-color: #e67e22;\n"
"    color: #a9b7c6;\n"
"    background-color: #e67e22;\n"
"}\n"
"QRadioButton::indicator:!checked {\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    border-style:solid;\n"
"    border-radius:5px;\n"
"    border-width: 1px;\n"
"    border-color: #e67e22;\n"
"    color: #a9b7c6;\n"
"    background-color: transparent;\n"
"}\n"
"QStatusBar {\n"
"    color:#34e8eb;\n"
"}\n"
"QSpinBox {\n"
"    color: #a9b7c6;    \n"
"    background-color:#000000;\n"
"}\n"
"QDoubleSpinBox {\n"
"    color: #a9b7c6;    \n"
"    background-color:#000000;\n"
"}\n"
"QComboBox {\n"
"    color: #a9b7c6;    \n"
"    background: #1e1d23;\n"
"}\n"
"QComboBox:editable {\n"
"    background: #1e1d23;\n"
"    color: #a9b7c6;\n"
"    selection-background-color:#000000;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    color: #a9b7c6;    \n"
"    background: #1e1d23;\n"
"    selection-color: #FFFFFF;\n"
"    selection-background-color:#000000;\n"
"}\n"
"QComboBox:!editable:on, QComboBox::drop-down:editable:on {\n"
"    color: #a9b7c6;    \n"
"    background: #1e1d23;\n"
"}\n"
"QFontComboBox {\n"
"    color: #a9b7c6;    \n"
"    background-color:#000000;\n"
"}\n"
"QToolBox {\n"
"    color: #a9b7c6;\n"
"    background-color:#000000;\n"
"}\n"
"QToolBox::tab {\n"
"    color: #a9b7c6;\n"
"    background-color:#000000;\n"
"}\n"
"QToolBox::tab:selected {\n"
"    color: #FFFFFF;\n"
"    background-color:#000000;\n"
"}\n"
"QScrollArea {\n"
"    color: #FFFFFF;\n"
"    background-color:#000000;\n"
"}\n"
"QSlider::groove:horizontal {\n"
"    height: 5px;\n"
"    background: #e67e22;\n"
"}\n"
"QSlider::groove:vertical {\n"
"    width: 5px;\n"
"    background: #e67e22;\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);\n"
"    border: 1px solid #5c5c5c;\n"
"    width: 14px;\n"
"    margin: -5px 0;\n"
"    border-radius: 7px;\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background: qlineargradient(x1:1, y1:1, x2:0, y2:0, stop:0 #b4b4b4, stop:1 #8f8f8f);\n"
"    border: 1px solid #5c5c5c;\n"
"    height: 14px;\n"
"    margin: 0 -5px;\n"
"    border-radius: 7px;\n"
"}\n"
"QSlider::add-page:horizontal {\n"
"    background: white;\n"
"}\n"
"QSlider::add-page:vertical {\n"
"    background: white;\n"
"}\n"
"QSlider::sub-page:horizontal {\n"
"    background: #e67e22;\n"
"}\n"
"QSlider::sub-page:vertical {\n"
"    background: #e67e22;\n"
"}\n")

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.setLayout(self.gridLayout)
        self.label = ImageLabel()
        self.label = QtWidgets.QLabel()
        self.label.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(60)
        sizePolicy.setVerticalStretch(50)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(600, 500))
        self.label.setMaximumSize(QtCore.QSize(2400, 2000))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label,2,0,5,5)
        self.label_2 = QtWidgets.QLabel()
        self.label_2.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(60)
        sizePolicy.setVerticalStretch(50)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(10, 50))
        self.label_2.setMaximumSize(QtCore.QSize(2400, 2000))
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(90)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 5)

        self.label_3 = QtWidgets.QLabel()
        self.label_3.setEnabled(True)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(60)
        sizePolicy.setVerticalStretch(50)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(10, 50))
        self.label_3.setMaximumSize(QtCore.QSize(2400, 2000))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 8, 3, 1, 2)

        self.pushButton = QtWidgets.QPushButton()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMaximumSize(QtCore.QSize(100, 80))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda: self.predict())
        self.gridLayout.addWidget(self.pushButton,8,0,1,2)

        fa5_icon = qta.icon('fa5s.upload', color='#FFFFFF')
        self.pushButton_1 = QtWidgets.QPushButton(fa5_icon,' Upload')

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_1.sizePolicy().hasHeightForWidth())
        self.pushButton_1.setSizePolicy(sizePolicy)
        self.pushButton_1.setMaximumSize(QtCore.QSize(100, 80))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_1.setFont(font)
        self.pushButton_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_1.setAutoFillBackground(False)

        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_1.clicked.connect(lambda: self.open())

        self.gridLayout.addWidget(self.pushButton_1, 7, 0, 1, 2)
        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setStyleSheet("QProgressBar{\n"
                                       "background-color: rgb(200, 200, 200);\n"
                                       "color: rgb(170, 85, 127);\n"
                                       "border-style: solid;\n"
                                       "border-radius: 10px;\n"
                                       "text-align: center;    \n"
                                       "}\n"
                                       "QProgressBar::chunk{\n"
                                       "border-radius: 10px;\n"
                                       "    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(185, 105, 254, 255), stop:1 rgba(106, 211, 255, 255));\n"
                                       "}")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar,8,1,1,2)
        self.progressBar.setVisible(False)
        ####################################
        self.index = 0
        self.fname = ""
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow", "Upload or Drag and Drop Photo here"))
        self.label_2.setText(_translate("MainWindow", "Face Shape Classifier"))
        self.label.setStyleSheet('''
                            QLabel{
                                border: 4px dashed #aaa
                            }
                        ''')
        self.label.setAcceptDrops(True)
        self.pushButton.setText(_translate("MainWindow", "Predict"))


    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            self.fname = event.mimeData().urls()[0].toLocalFile()
            self.set_image(self.fname)
            self.label_3.setText("")
            self.progressBar.setValue(0)
            self.progressBar.setVisible(False)
            event.accept()
        else:
            event.ignore()

    def set_image(self, file_path):
        self.pixmap = QPixmap(file_path)
        self.pixmap = self.pixmap.scaled(QtCore.QSize(self.label.width(), self.label.height()), Qt.KeepAspectRatio,
                                         Qt.SmoothTransformation)
        self.label.setStyleSheet("border:none;")
        self.label.setPixmap(QPixmap(self.pixmap))


    def open(self):
        self.fname = QFileDialog.getOpenFileName(None, 'Open png', QtCore.QDir.rootPath(),
                                            'All files(*)')
        self.fname = self.fname[0]
        ###open the image
        self.set_image(self.fname)
        self.label_3.setText("")
        self.progressBar.setValue(0)
        self.progressBar.setVisible(False)


    def landmarks(self):
        img = cv2.imread(self.fname)
        model=Landmarks(img)
        rectangles=model.detect_faces()
        landmarks=model.detect_landmarks(rectangles)

        image_with_rectangles=model.apply_rectangles(img,rectangles) 
        self.image_with_both= model.apply_landmarks(image_with_rectangles,landmarks) #draw landmarks on image with rectangles

    def predict(self):
        self.progressBar.setVisible(True)   
        #mode = 0o666
        #read image 
        img=cv2.cvtColor(cv2.imread(self.fname), cv2.COLOR_BGR2RGB)
        #predict landmarks
        rectangles=landmarks_model.detect_faces(img)
        landmarks=landmarks_model.detect_landmarks(img,rectangles)
        image_with_rectangles=landmarks_model.apply_rectangles(img,rectangles) 
        self.image_with_both= landmarks_model.apply_landmarks(image_with_rectangles,landmarks) #draw landmarks on image with rectangles
	#progress bar loop
        for i in range(101):
            # slowing down the loop
            time.sleep(0.012)
            # setting value to progress bar
            self.progressBar.setValue(i)
        #transform image to dataset
        train_ds=Dataset.from_dict({"image":[Image.fromarray(self.image_with_both)],"label":[0]})
        train_ds.set_transform(train_transforms)
        ###### convert photo from numpy array to pyqt image
        image = Image.fromarray(self.image_with_both, mode='RGB')
        self.qt_img = ImageQt.ImageQt(image)
        ####### convert from pyqt image into pixmap image
        self.pixmap = QtGui.QPixmap.fromImage(self.qt_img)
        self.pixmap = self.pixmap.scaled(QtCore.QSize(self.label.width(), self.label.height()), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setStyleSheet("border:none;")
        self.label.setPixmap(QPixmap(self.pixmap))
        #predict faceshape
        outputs = trainer.predict(train_ds)
        y_pred = outputs.predictions.argmax(1)
        self.progressBar.setVisible(False)
        self.label_3.setText(f"Face Shape is: {shapes[y_pred[0]]}")



app = QApplication(sys.argv)
demo = Ui_MainWindow()
demo.show()
sys.exit(app.exec_())