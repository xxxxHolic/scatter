#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 23:58:17 2018

@author: user
"""

import numpy  as np
import pandas as pd

import matplotlib.pyplot as plt

#########################  CONSTANT ###############################

########### RGB COLORS ############


RGB1 = {'black'  :[  0,  0,  0],
        'white'  :[255,255,255],
        'red'    :[255,  0,  0],
        'green'  :[  0,255,  0],
        'blue'   :[  0,  0,255],
        'yellow' :[255,255,  0],
        'cyan'   :[  0,255,255],
        'magenta':[255,  0,255]}

RGB2 = {'k'      :[  0,  0,  0],
        'w'      :[255,255,255],
        'r'      :[255,  0,  0],
        'g'      :[  0,255,  0],
        'b'      :[  0,  0,255],
        'y'      :[255,255,  0],
        'c'      :[  0,255,255],
        'm'      :[255,  0,255]}

v = pd.read_csv('test.csv')['5.3987'].tolist()


#########################  FUNCTIONS ###############################

##### grayscale affine transformation ######

### linear transformation ###
def linear(value_list, mode = 0):

    'linear transform the origin data'
    
    v_min = np.min(value_list)
    v_list = (value_list - v_min)/np.max(value_list - v_min)    
    
    # show data
    if mode:
        plt.plot(np.array(v_list)[np.argsort(v_list)])
        
    return v_list

### gamma transformation ###
def imadjust(value_list, gamma, low_in=0, high_in=1, low_out=0, high_out=1, mode=0):

    'gamma transform the origin data'

    # linear transform the data first
    v_min = np.min(value_list)
    v_list  = np.array((value_list - v_min)/np.max(value_list - v_min))
    
    # set the range of the value
    l_vlist = v_list >= low_in           # bool data higher than low in
    r_vlist = v_list <= high_in          # bool data lower than high in
    s_vlist = l_vlist*r_vlist            # bool data between lowin and highin
    
    v_lt = v_list[v_list <= low_in]      # value lower than low in
    v_rt = v_list[v_list >= high_in]     # value higher than high in
    v_in = v_list[s_vlist]               # value between the range
    
    # re linear transform the data between low_in and high_in to 0-1
    v_in_expand = (v_in - np.min(v_in))/np.max(v_in - np.min(v_in))
    # gamma apply
    v_in_gamma = v_in_expand**gamma
    # re linear transform to out data between low_out and high_out
    v_ot = (v_in_gamma + low_out/(high_out - low_out))*(high_out - low_out)
    # re linear transform v_lt to v_ot_lt (lower than low_out)
    if low_in == 0:
        v_ot_lt = v_lt
    else:
        v_ot_lt = v_lt*(low_out/low_in)
    # re linear transform v_rt to v_ot_rt (higher than high_out)
    v_ot_rt = (v_rt-1)*((1-high_out)/high_in) + 1
    
    v = np.zeros(len(value_list))
    
    v[s_vlist] = v_ot
    v[v_list >= high_in] = v_ot_rt
    v[v_list <= low_in] = v_ot_lt
    
    # show data
    if mode:
        plt.plot(np.array(v)[np.argsort(v)])
    
    v_list = v
    return v_list

### log transformation ###
def logit(value_list, mode = 0):
    
    'log transform the origin data'
    
    # log transform data
    v = np.log(value_list + np.min(value_list)*1e-3)
    # linear transform to 0-1
    v_min = np.min(v)
    v_list = (v - v_min)/np.max(v - v_min) 
    
    # show data
    if mode:
        plt.plot(np.array(v_list)[np.argsort(v_list)])
    
    return v_list

### strech transformation ###
def strech(value_list, e = 1, mode = 0):
    
    'strech transform the origin data'
    
    # strech transform the origind data
    v = 1/(1 + (np.mean(value_list)/value_list)**e)
    # linear transform the origin data
    v_min = np.min(v)
    v_list = (v - v_min)/np.max(v - v_min) 
    
    # show data
    if mode:
        plt.plot(np.array(v_list)[np.argsort(v_list)])
    
    return v_list

### gauss transformation ###
def gausst(value_list, height, width, center, mode = 0):
    
    'strech transform the origin data'
    
    if isinstance(height,int) and isinstance(width,int) and isinstance(center,int):
        center = [center]
        width  = [width]
        height = [height]

    elif len(height) != len(width) or len(height) != len(center) or len(width) != len(center):
        raise ValueError('The list center,width and height should be equal length!')
        
    else:
        pass
        
    v = np.zeros(len(value_list))
    index = 0
    
    for peak in center:
        v = v + height[index]*np.exp((np.array(value_list) - peak)**2/width[index]**2)
        index += 1
    
    v_min = np.min(v)
    v_list = (v - v_min)/np.max(v - v_min)
        
    # show data
    if mode:
        plt.plot(np.array(v_list)[np.argsort(v_list)])
        
    return v_list
        
############### hist calculation ##################

### histgram calculate ###
def hist(value_list, g = 65535, mode = 0):
    
    'calculate and plot histgram'
    
    # check if import is interger
    if not isinstance(g, int):
        raise ValueError('g should be an interger')
    
    # linear transformation    
    v_min = np.min(value_list)
    v = (value_list - v_min)/np.max(value_list - v_min)
    
    # get the pixel number between n/g and (n+1)/g
    def hist_range(vl, n):
        
        # set the range of the value
        lv = vl >= n/g               # bool data higher than low in
        rv = vl <= (n+1)/g           # bool data lower than high in
        sv = lv*rv                   # bool data between lowin and highin
        
        v_in = vl[sv]                # value between the range
    
        return len(v_in)
    
    hist_list = np.zeros(g)
    # get hist
    for pixel in range(g):
        hist_list[pixel] = hist_range(v, pixel)
        
    if mode:
        plt.bar(range(g), hist_list)
        
    return hist_list

### hist_equal transformation ###
def hist_equal(value_list, g=65535, mode=0):

    'hist equal transformation'

    if not isinstance(g, int):
        raise ValueError('g should be an interger')
        
    v_min = np.min(value_list)
    v = (value_list - v_min)/np.max(value_list - v_min)
    
    # hist_range for histeq
    def hist_range_eq(vl, n):
        
        # set the range of the value
        lv = vl >= n/g               # bool data higher than low in
        rv = vl <= (n+1)/g           # bool data lower than high in
        sv = lv*rv                   # bool data between lowin and highin
        
        v_in = vl[sv]                # value between the range
    
        return len(v_in), sv
    
    hist_list = np.zeros(g, dtype = int)    # hist list
    hist_bool = np.zeros(g, dtype = int)    # hist bool
    hist_posi = np.zeros(g, dtype = list)   # the poisition of the data between n/g and (n+1)/g
    
    for pixel in range(g):
        # calculte hist and return number , position
        num, position = hist_range_eq(v, pixel)
        
        hist_list[pixel] = num
        hist_bool[pixel] = bool(num)
        hist_posi[pixel] = position
        
    min_cdf = np.min(hist_list[hist_bool == 1])
    hist_non0 = np.nonzero(hist_bool)[0]
    index = 0
    
    # hist equal trasnform
    for index in range(len(hist_non0)):
        
        cdf = np.sum(hist_list[hist_non0[0:index]])
        position_cdf = hist_posi[hist_non0[index]]
        v[position_cdf] = (cdf - min_cdf)/(len(v) - min_cdf)
        
    return v
    
########### COLOR MAPS ############

### jet color bar ###
def jet(value):
    
    value = 4*value/256
    
    r = 255*np.min(np.max(np.min(value -1.5,-value +4.5), 0), 1);
    g = 255*np.min(np.max(np.min(value -0.5,-value +3.5), 0), 1);
    b = 255*np.min(np.max(np.min(value +0.5,-value +2.5), 0), 1);
    
    return [r, g, b]

