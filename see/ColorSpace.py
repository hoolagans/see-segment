import copy
import inspect
import random

from collections import OrderedDict
import sys
import logging
import numpy as np
import skimage
from skimage import color
from see.base_classes import param_space, algorithm

param_space.add('colorspace', 
                ['RGB', 'HSV', 'RGB CIE', 'XYZ', 'YUV', 'YIQ', 'YPbPr', 'YCbCr', 'YDbDr'],
                "Pick a colorspace [‘RGB’, ‘HSV’, ‘RGB CIE’, ‘XYZ’, ‘YUV’, ‘YIQ’, ‘YPbPr’, ‘YCbCr’, ‘YDbDr’]"
               )
param_space.add('multichannel',
                [True, False],
                "True/False parameter")
param_space.add('channel',
                [0,1,2],
                "A parameter for Picking the Channel 0,1,2"
               )

class colorspace(algorithm):
    
    def getchannel(img, colorspace, channel):
        """function that returns a single channel from an image
        ['RGB', ‘HSV’, ‘RGB CIE’, ‘XYZ’, ‘YUV’, ‘YIQ’, ‘YPbPr’, ‘YCbCr’, ‘YDbDr’]
        """
        dimention=3;
        if (len(img.shape) == 2):
            c_img = img.copy();
            img = np.zeros([c_img.shape[0], c_img.shape[1],3])
            img[:,:,0] = c_img;
            img[:,:,1] = c_img;
            img[:,:,2] = c_img;
            return [img, c_img, 1]

        if(colorspace == 'RGB'):
            return [img, img[:,:,channel], 3]
        else:
            space = color.convert_colorspace(img, 'RGB', colorspace)
            return [space, space[:,:,channel], 3]
    
    ##TODO Update to allow paramlist to be either a list or the parameters class
    def __init__(self, paramlist=None):
        """Generate algorithm params from parameter list."""
        self.params = param_space()
        self.params['colorspace'] = 'RGB'
        self.params['multichannel'] = True
        self.params['channel'] = 2
        
        self.chache = dict()
        if paramlist:
            self.params.fromlist(paramlist)
        else:
            self.params["multichannel"] = True
            self.params["colorspace"] = "RGB"
            self.params["channel"] = 2
        self.paramindexes = ["colorspace", "multichannel", "channel"]
        self.checkparamindex()
    
    #TODO use name to build a dictionary to use as a chache
    def evaluate(self, img, name=None):
        """Run segmentation algorithm to get inferred mask."""
        
        multichannel = self.params['multichannel']
        
        if len(img.shape) > 2:
            multichannel = False
        
        [img, channel, dimention] = colorspace.getchannel(img, self.params['colorspace'], self.params['channel']) 
        
        if multichannel:
            return img
        else:
            return channel