# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 05:59:46 2018

@author: zefa
"""

import os
import numpy as np
import cv2


MAX_HEIGHT = 720


def apply_mask(image, mask, color, alpha=0.5):
    """Apply the given mask to the image.
    """
    for c in range(3):
        image[:, :, c] = np.where(mask == 1,
                                  image[:, :, c] *
                                  (1 - alpha) + alpha * color[c] * 255,
                                  image[:, :, c])
    return image



class SequenceControl(object):
    
    def __init__(self, path=None):
        self.name = 'not set'
        self.path = path
        self.max_height = float(MAX_HEIGHT)
        
    def getName(self):
        """
        Returns the name of the sequence.
        """
        return self.name

    def numberOfImages(self):
        """ 
        Returns the number of images in the video.
        """
        return self.frameCount
   
    def currentFrameNumber(self):
        """ 
        Returns the current frame number.
        """
        return self.fNr
    
    def getImage(self):
        """
        Returns the current image of the video or None if video is None.
        """
        return self.img

    def loadImage(self, fNr, labels, result=None):
        """
        Load the selected (fNr) image. Has to be reimplemented by child class.
        """
        raise NotImplementedError

    def _processImage(self, img, labels, result):
        # set rgb ordering
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if result is not None:
            self._labelInstances(img, labels, result)
        # scale if necessary
        if self.scale != 1:
            img = cv2.resize(img, None, fx=self.scale, fy=self.scale)
        return img
        
    def _labelInstances(self, image, labels, result):
        """
        boxes: [num_instance, (y1, x1, y2, x2, class_id)] in image coordinates.
        masks: [height, width, num_instances]
        class_ids: [num_instances]
        """
        # get the data
        boxes, masks, class_ids, scores = [result[k] for k in ['rois','masks','class_ids','scores']]
        selected_ids = [l.getClassIndex() for l in labels]
        
        # Number of instances
        N = boxes.shape[0]
        if not N:
            print("\n*** No instances to display *** \n")
        else:
            assert boxes.shape[0] == masks.shape[-1] == class_ids.shape[0]
    
    
        for i in range(N):
            if not np.any(boxes[i]):
                continue
            
            if class_ids[i] not in selected_ids:
                continue
            
            col = labels[selected_ids.index(class_ids[i])].getColor()
            # add mask
            image = apply_mask(image, masks[:,:,i], col, alpha=0.4)
    
        return image

    def __iter__(self):
        raise NotImplementedError
        
        