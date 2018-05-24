# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 05:59:46 2018

@author: zefa
"""

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QSizePolicy

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure

#from matplotlib import rcParams
#rcParams['font.size'] = 9

import seaborn as sns

FS_AXES = 8


class HistPlotQWidget(Canvas):
    """
    HistPlotQWidget for plotting simple histograms.
    """
    
    def __init__(self, parent=None, width=5, height=3, dpi=120, hold=False):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.figure.add_subplot(111)
        self.axes.hold(hold)

        Canvas.__init__(self, self.figure)
        self.setParent(parent)

        Canvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        Canvas.updateGeometry(self)
        
        self.canvas = self.axes.figure.canvas

    def sizeHint(self):
        w, h = self.get_width_height()
        return QSize(w, h)

    def minimumSizeHint(self):
        return QSize(200, 150)
            
    def plot(self, data):
        self._update(self.axes, data)
        self.canvas.draw_idle()
        
    def _update(self, ax, data):
        sns.distplot(data, bins=100, kde=False, ax=ax)
        ax.tick_params(axis='y', labelsize=FS_AXES)
        ax.tick_params(axis='x', labelsize=FS_AXES)
        #ax.set_title(sel_features[0] + ' vs. ' + sel_features[1], fontsize=FS_TITLE)
        ax.grid('on')
        ax.figure.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.12)
        
        


