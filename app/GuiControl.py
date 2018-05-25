# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 05:59:46 2018

@author: zefa
"""

import os
import numpy as np
import pickle
import lzma
import importlib

from .VideoControl import VideoControl
from .ImageSequenceControl import ImageSequenceControl
from .Label import Label
from .helper import get_colors
from .config import get_class_labels, class_names, MINIMAL_FREQ


SAVE_RESULT_TEMPORARY = True


class GuiControl(object):
    
    def __init__(self):
        self.stats = None
        self.result = None
        self.instanceSegModel = None
        # check if we find the mask rcnn package
        if importlib.util.find_spec("mrcnn") is not None:
            from .MaskRCNN import MaskRCNN
            self.instanceSegModel = MaskRCNN()
        # update labels
        self._update_labels()
        

    def open(self, path):
        """
        Open new image source.
        """
        if path.endswith('.jpg') or path.endswith('.png'):    
            self.seq_ctrl = ImageSequenceControl(path)
        else:
            self.seq_ctrl = VideoControl(path)
            
        # search for corresponding stats file
        if path is not None:
            result_file = path.rsplit('.', 1)[0] + '.pkl'
            if os.path.exists(result_file):
                self._load_stats(result_file)
        
        # update labels
        self._update_labels()
        
    def getStats(self, label):
        """
        Returns the frames the specified class of objects occured.
        """
        if self.stats is None:
            return
        
        if label is None:
            label = self.labels[0]
            
        return np.array(self.instances[label.getClass()])
        
    def getName(self):
        """
        Returns the name of the video.
        """
        return self.seq_ctrl.getName()

    def numberOfImages(self):
        """ 
        Returns the number of images in the video.
        """
        return self.seq_ctrl.numberOfImages()
    
    def currentFrameNumber(self):
        """ 
        Returns the current frame number.
        """
        return self.seq_ctrl.currentFrameNumber()
    
    def getImage(self):
        """
        Returns the current image of the video or None if video is None.
        """
        return self.seq_ctrl.getImage()
    
    def gotoImage(self, fNr):
        """
        Returns the current image of the video or None if video is None.
        """
        # search for precalculated result file 
        self._load_result(fNr)
        # load image and color it.
        self.seq_ctrl.loadImage(fNr, self.labels, self.result)

    def getLabels(self):
        """
        Returns the set of labels ordered by frequency if possible.
        """
        return self.labels

    def processImage(self):
        """
        Analyse image using mask-RCNN and color current frame accordingly.
        """
        if self.instanceSegModel is None:
            return
        
        fNr = self.seq_ctrl.currentFrameNumber()

        self.result = self.instanceSegModel.processImage(self.seq_ctrl.getImage())
        if SAVE_RESULT_TEMPORARY:
            self._save_result(fNr, self.result)
            
        # apply coloring
        self.seq_ctrl.loadImage(fNr, self.labels, self.result)

    def processImageSequence(self):
        """
        Analyse all images in the sequence/video using the mask-RCNN framework.
        """
        if self.instanceSegModel is None:
            return

        for fNr, image in enumerate(self.seq_ctrl):
            print('processing image %i ...' % fNr)
            result = self.instanceSegModel.processImage(image)
            if SAVE_RESULT_TEMPORARY:
                self._save_result(fNr, result)

    def _load_stats(self, result_file):
        """
        Open corresponding stats file and process it.
        """
        with open(result_file, 'rb') as fp:
            self.stats = pickle.load(fp)
            # create lookup table                
            self.instances = {}
            for frn, itm in enumerate(self.stats):
                for id_ in itm['class_ids']:
                    self.instances.setdefault(class_names[id_], []).append(frn)

    def _load_result(self, fNr):
        """
        Open corresponding stats file and process it.
        """
        self.result = None        
        if fNr < 0:
            return
        
        base_name = self.seq_ctrl.getName()
        mask_file = 'tmp/%s/res_%04i.xz' % (base_name, fNr)
        if os.path.exists(mask_file):
            with lzma.open(mask_file, 'rb') as fp:
                self.result = pickle.load(fp)
                
    def _save_result(self, fNr, result):
        """
        Open corresponding stats file and process it.
        """
        base_name = self.seq_ctrl.getName()
        temp_dir = os.path.join('tmp', base_name)
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)

        mask_file = os.path.join(temp_dir, 'res_%04i.xz' % fNr)
        with lzma.open(mask_file, 'wb') as fp:
            pickle.dump(result, fp, -1)

    def _update_labels(self):
        """
        Updates the labels to focus on.
        """
        self.labels = []
        if self.stats is not None:
            lbls = sorted(self.instances.keys())
            idx = np.argsort([len(self.instances[k]) for k in lbls])[::-1]
            
            colors = get_colors(len(idx))
            for c, i in enumerate(idx):
                freq = float(len(self.instances[lbls[i]])) / len(self.stats)
                if freq < MINIMAL_FREQ:
                    break
                
                cls_idx = class_names.index(lbls[i])
                self.labels.append(Label(cls_idx, lbls[i], colors[c], freq))
        else:
            labels = get_class_labels()
            colors = get_colors(len(labels))
            for i, lbl in enumerate(labels):
                cls_idx = class_names.index(lbl)
                self.labels.append(Label(cls_idx, lbl, colors[i]))

