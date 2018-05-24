# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 05:59:46 2018

@author: zefa
"""

import os
import numpy as np
import cv2
import glob

from .SequenceControl import SequenceControl


class ImageSequenceControl(SequenceControl):
    
    def __init__(self, path=None):
        super(ImageSequenceControl, self).__init__(path)
        self._init(path)
    
    def _init(self, path):
        """ 
        Open the video file and load first frame to image variable
        """
        data_dir  = os.path.dirname(path)
        extension = path.rsplit('.', 1)[1]
        self.img_fns = sorted(glob.glob(os.path.join(data_dir, '*.'+extension)))
        
        self.frameCount = len(self.img_fns)
        self.scale = 1
        
        if self.frameCount > 0:
            img = cv2.imread(self.img_fns[0])
            w = img.shape[0]
            h = img.shape[1]
            if h > self.max_height:
                self.scale = self.max_height / h
            print(w, h, self.scale)
            
        # load first image
        self.loadImage(0, [])

        # create name for displaying in gui. We take the dir name where the images
        # are located
        self.name = os.path.split(data_dir)[1]

    def loadImage(self, fNr, labels, result=None):
        """
        Open the selected image of the sequence or create empty one.
        """
        if fNr >= 0 and fNr < self.frameCount:
            self.fNr = fNr
            img = cv2.imread(self.img_fns[self.fNr])
            self.img = self._processImage(img, labels, result)
        else:
            self.img = np.zeros((720, 1280, 3), dtype=np.uint8)
            self.fNr = -1

    def __iter__(self):
        for i in range(self.frameCount):
            img = cv2.imread(self.img_fns[i])
            yield img

