# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 05:59:46 2018

@author: zefa
"""

import os
import cv2
import numpy as np

from .SequenceControl import SequenceControl


class VideoControl(SequenceControl):
    
    def __init__(self, path=None):
        super(VideoControl, self).__init__(path)
        self._init(path)
    
    def _init(self, path):
        """ 
        Open the video file and load first frame to image variable
        """
        self.vid = cv2.VideoCapture(path)

        self.frameCount = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
        w = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.scale = 1
        if h > self.max_height:
            self.scale = self.max_height / h
            print(w, h, self.scale)
            
        # load first image
        self.loadImage(0, [])
        
        # create name for displaying in gui
        if path is not None:
            self.name = os.path.basename(path).rsplit('.', 1)[0]

    def loadImage(self, fNr, labels, result=None):
        """
        Load the selected (fNr) image of the video or create empty one.
        """
        self.fNr = fNr
        self.vid.set(cv2.CAP_PROP_POS_FRAMES, self.fNr)
        retv, img = self.vid.read()
        if not retv:
            self.img = np.zeros((720, 1280, 3), dtype=np.uint8)
            self.fNr = -1
        else:
            self.img = self._processImage(img, labels, result)

    def __iter__(self):
        self.vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
        for i in range(self.frameCount):
            retv, img = self.vid.read()
            yield img
            
            
            
