# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 05:11:54 2018

@author: zefa
"""

import sys 
from PyQt5 import QtCore, QtGui, QtWidgets

from UI.main_win import Ui_MainWindow
from UI.LabelQWidget import LabelQWidget
from UI.HistPlotQWidget import HistPlotQWidget
from app.GuiControl import GuiControl
from app.helper import toQImage



class ISegViewerApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setupActions()
        self.setupPlotWidget()
        self.ctrl = GuiControl()

    def setupActions(self):
        self.actionOpen.triggered.connect(self.open)
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.about)
        self.frameSlider.valueChanged.connect(lambda frm: self.setFrame(frm))
        self.listWidget_Labels.itemSelectionChanged.connect(self.labelSelected)

    def setupPlotWidget(self):
        self.histPlotWidget = HistPlotQWidget(self)
        self.verticalLayout_Timeline.addWidget(self.histPlotWidget)
        self.histPlotWidget.hide()

    def updatePlotWidget(self, label=None):
        data = self.ctrl.getStats(label)
        if data is not None:
            self.histPlotWidget.show()
            self.histPlotWidget.plot(data)

    def labelSelected(self):
#        idx = self.listWidget_Labels.selectedIndexes()
#        item = self.listWidget_Labels.itemAt(idx[0])
        for i in range(self.listWidget_Labels.count()):
            item = self.listWidget_Labels.item(i)
            if item.isSelected():
                labelWidget = self.listWidget_Labels.itemWidget(item)
                self.updatePlotWidget(labelWidget.classLabel)                
                break
        
    def updateListControl(self):
        """
        Add new entry to workspace list.
        """
        self.listWidget_Labels.clear()
        for lbl in self.ctrl.getLabels():
            self.createLabelEntry(lbl)
        
    def createLabelEntry(self, label):
        """
        Add new entry to workspace list.
        """
        # Create workspace Widget
        myQCustomQWidget = LabelQWidget(self, label)
        # Create QListWidgetItem
        myQListWidgetItem = QtWidgets.QListWidgetItem(self.listWidget_Labels)
        # Set size hint
        myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
        # Add QListWidgetItem into QListWidget
        self.listWidget_Labels.addItem(myQListWidgetItem)
        self.listWidget_Labels.setItemWidget(myQListWidgetItem, myQCustomQWidget)        
        
    def about(self):
        QtWidgets.QMessageBox.about(self, "About ImSegU",
                "<p>The <b>Image Segmentation & Understanding</b> app uses"
                "instance segmentation to extract semantical information "
                "from the images of a video or image sequence.</p>")

    def open(self):
        file_types = "Videos|Imgs (*.avi *.mp4 *.jpg *.png)"
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File",
                QtCore.QDir.currentPath(), file_types)
        if fileName:
            self.ctrl.open(fileName)
            self.setFrame(0)
            self.updateListControl()
            self.updatePlotWidget()
            
            if self.ctrl.numberOfImages() <= 0:
                QtWidgets.QMessageBox.information(self, "Image Viewer",
                        "Cannot load %s." % fileName)
                return

    def setFrame(self, frameNumber):
        self.ctrl.gotoImage(frameNumber)
        image = toQImage(self.ctrl.getImage())
        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))
        self.updateSlider()
        
#    def updateImage(self):
#        image = toQImage(self.ctrl.currentImage())
#        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))

    def updateSlider(self):
        f = self.ctrl.currentFrameNumber()
        length = self.ctrl.numberOfImages()
        self.sliderLabel.setText('%i / %i' % (f+1, length))
        if length > 0:
            self.frameSlider.setMinimum(0)
            self.frameSlider.setMaximum(length-1)
    
    def processImage(self):
        self.ctrl.processImage()
        
    def processImageSequence(self):
        self.ctrl.processImageSequence()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_F5:
            self.processImage()
        elif e.key() == QtCore.Qt.Key_F8:
            self.processImageSequence()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = ISegViewerApp()
    form.show()
    app.exec_()
