# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 06:28:00 2018

@author: zefa
"""

import numpy as np
import colorsys
from PyQt5 import QtGui


class NotImplementedException:
    pass


initialColors = ['darkGreen','darkBlue','darkMagenta','darkCyan','darkYellow','darkGray']

def get_colors(N, bright=True):
    """
    Generate random colors.
    To get visually distinct colors, generate them in HSV space then
    convert to RGB.
    """
    brightness = 1.0 if bright else 0.7
    hsv = [(i / N, 1, brightness) for i in range(N)]
    colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    return colors



def toQImage(im, copy=False):
    if im is None:
        return QtGui.QImage()

    if im.dtype == np.uint8:
        if len(im.shape) == 2:
            qim = QtGui.QImage(im.data, im.shape[1], im.shape[0], im.strides[0], 
                               QtGui.QImage.Format_Indexed8)
            gray_color_table = [QtGui.qRgb(i, i, i) for i in range(256)]
            qim.setColorTable(gray_color_table)
            return qim.copy() if copy else qim

        elif len(im.shape) == 3:
            if im.shape[2] == 3:
                qim = QtGui.QImage(im.data, im.shape[1], im.shape[0], im.strides[0], 
                                   QtGui.QImage.Format_RGB888);
                return qim.copy() if copy else qim
            elif im.shape[2] == 4:
                qim = QtGui.QImage(im.data, im.shape[1], im.shape[0], im.strides[0], 
                                   QtGui.QImage.Format_ARGB32);
                return qim.copy() if copy else qim

    raise NotImplementedException
