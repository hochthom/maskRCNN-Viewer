#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 22 17:49:15 2018

@author: tola
"""



class Label(object):
    
    def __init__(self, idx, label, color, freq=None):
        self.label = label
        self.class_idx = idx
        self.color = color
        self.freq = freq
        self.visible = True

    def getClass(self):
        return self.label
    
    def getClassIndex(self):
        return self.class_idx
    
    def info(self):
        if self.freq is not None:
            return '%4.1f  %s' % (self.freq, self.label)
        return self.label
    
    def getColor(self):
        return self.color
    
    def changeColor(self, color):
        self.color = color

    def hide(self):
        self.visible = False
        
    def show(self):
        self.visible = True

