# -*- coding: utf-8 -*-
#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Copyright (C) Software Competence Center Hagenberg GmbH (SCCH)
# All rights reserved.
# -----------------------------------------------------------------------------
# This document contains proprietary information belonging to SCCH.
# Passing on and copying of this document, use and communication of its
# contents is not permitted without prior written authorization.
# -----------------------------------------------------------------------------
# Created on $Date: 2014-04-08 17:45:44 +0200 (Do, 08 Apr 2014) $ 
# by $Author: mdorfer $
# SVN $Rev: $
#

# --- imports -----------------------------------------------------------------

import qtawesome as qta

from PyQt5 import QtCore, QtGui, QtWidgets    
    
    
class LabelQWidget (QtWidgets.QWidget):
    def __init__(self, parent, label):
        super(LabelQWidget, self).__init__(parent)
        self.classLabel = label

        self.allQHBoxLayout  = QtWidgets.QHBoxLayout()
        self.allQHBoxLayout.setContentsMargins(1,1,1,1)
        
        # create UI
        self.colorBox = QtWidgets.QPushButton('')
        self.colorBox.setFixedSize(20,20)
        color = QtGui.QColor(*label.getColor())
        style = "background-color:%s; border: 1px solid #ffffff" % color.name()
        self.colorBox.setStyleSheet(style)
        self.colorBox.clicked.connect(self.onChoseColor)

        self.textLabel = QtWidgets.QLabel(label.info())
        # setStyleSheet
        self.textLabel.setStyleSheet('''
            color: rgb(0, 0, 0);
            font-weight: bold;
            font-size: 12px;
        ''')

        view_icon = qta.icon('fa.eye', color='green')
        self.viewBtn = QtWidgets.QPushButton(view_icon, '')
        self.viewBtn.setFixedSize(20,20)
        self.viewBtn.setCheckable(True)
        self.viewBtn.clicked.connect(lambda:self.hideLabel(self.viewBtn))

        self.allQHBoxLayout.addWidget(self.colorBox)
        self.allQHBoxLayout.addWidget(self.textLabel, 1)
        self.allQHBoxLayout.addWidget(self.viewBtn)        
        self.setLayout(self.allQHBoxLayout)

    def hideLabel(self, btn):
        if btn.isChecked():
            view_icon = qta.icon('fa.eye-slash', color='black')
            self.classLabel.hide()
        else:
            view_icon = qta.icon('fa.eye', color='green')
            self.classLabel.show()
        btn.setIcon(view_icon)

    def setColor(self, color):
        self.colorBox.setStyleSheet("background-color:%s; border: 1px solid #ffffff" % color)
        
    @QtCore.pyqtSlot()
    def onChoseColor(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.classLabel.changeColor(color.getRgb())
            self.setColor(color.name())
        


