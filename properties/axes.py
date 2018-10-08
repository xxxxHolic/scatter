#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 17:44:56 2018

@author: user
"""

import numpy  as np

def axes(qx,qy,qz,center,zoom,ratio):

    
    #if center == [0, 0, 0]:
    cx = (np.min(qx) + np.max(qx))/2
    cy = (np.min(qy) + np.max(qy))/2
    cz = (np.min(qz) + np.max(qz))/2
    #else:
    
    # transform the data to center 0,0,0
    # add ratio
    px = (np.array(qx) - cx)*ratio[0]
    py = (np.array(qy) - cy)*ratio[1]
    pz = (np.array(qz) - cz)*ratio[2]
    
    limit = np.max([np.max(px), np.max(py), np.max(pz)])
    
    # limit data to 0-1
    # add zoom
    px = (9/16)*(px/limit)*zoom
    py = (9/16)*(py/limit)*zoom
    pz = (9/16)*(pz/limit)*zoom
    
    # add center
    px = px - center[0]
    py = py - center[1]
    pz = pz - center[2]
    
    position = np.zeros([len(px),3])
    position[:,0] = px
    position[:,1] = py
    position[:,2] = pz
    
    return position
    



    
