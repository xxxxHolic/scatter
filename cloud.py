#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 23:29:53 2018

@author: user
"""

# Codes are free to use. Do whatever you want

from __future__ import absolute_import

"""point cloud"""

####################### LIBRARY #############################

# exceptions library

# Python stdlib imports

# data processing library
import numpy  as np

# opengl api
from glumpy import app, gl, gloo, glm

# pyrod library
from properties import axes, color, shader

####################### CONSTANT ############################
        
####################### FUNCTIONS ###########################

# painting RGBA colors to value
def painting(color_bar, face_color, value, transparent, n):
    
    if color_bar == 'pure':
        color_e = color.RGB1[face_color]
    elif color_bar == 'maps':
        color_e = color.jet(value)
    
    colors = np.zeros([n, 4])
    
    colors[:,0] = color_e[0]
    colors[:,1] = color_e[1]
    colors[:,2] = color_e[2]
    colors[:,3] = np.array(value)*transparent
    
    return colors

######################## CLASSS #############################

class cloud(object):
    
    def __init__(self, qx, qy, qz, qi):
        
        self.qx = qx
        self.qy = qy
        self.qz = qz
        self.qi = qi
        
        if len(qx) == len(qy) == len(qz) == len(qi):
            pass
        else:
            raise ValueError('Import qx, qy, qz, qi must be equal length!')
        
        self.position = np.zeros([len(qi), 3])
        
        # shader
        self.vertex = shader.vertex_point      # vertex shader
        self.fragment = shader.fragment_point  # fragment shader
        
        # color
        self.face_color = 'blue'               # point color
        self.back_color = 'white'              # background color
        self.back_alpha = 1                    # background transparent
        self.color_bar = 'pure'                # 'pure' for pure color,'jet' for jet color map
        self.color = np.zeros([len(qi), 4])    # RGBA color
        self.transparent = 10                  # transparent of points
        # transformation
        self.transform = 'linear'              # data transformation, default method is linear transform
        
        # apperance 
        self.theta = 20                        # default theta value
        self.phi = 0                           # default phi value
        self.chi = -50                         # default chi value
        self.r_theta = 0                       # default rotate theta value
        self.r_phi = 0                         # default rotate phi value
        self.r_chi = 0                         # default rotate chi value
        self.window_width = 500                # default window width
        self.window_height = 500               # default window height
        self.r = 1                             # default point radius
        
        # axis
        self.translate = -2.5
        self.center = [0,0,0]
        self.zoom = 1
        self.ratio = [1,1,1]
        
        # light
        self.light = [1,1,1]
        
    def __repr__():
        return 'cloud: initialize the data for visualization'
    
    def __str__(self):
        
        print('--------------------------\n' + 
              'cloud: initialize the data for visualization \n' + 
              '\n'+               
              'RECIPROCAL SPACE \n' + 
              'limit_x: %s - %s \n' %(np.min(self.qx), np.max(self.qx))+ 
              'limit_y: %s - %s \n' %(np.min(self.qy), np.max(self.qy))+ 
              'limit_z: %s - %s \n' %(np.min(self.qz), np.max(self.qz))+ 
              '\n' + 
              'VIEW \n' + 
              'theta: %s r_theta: %s \n' %(self.theta, self.r_theta)+
              'phi: %s   r_phi: %s \n'   %(self.phi, self.r_phi)+
              'chi: %s   r_chi: %s \n'   %(self.chi, self.r_chi)+
              '\n' +
              'COLOR \n' +
              'point color: %s \n'       %(self.face_color)+
              'backgroud color: %s \n'   %(self.back_color)+
              'back transparent: %s \n'  %(self.back_alpha)+
              '\n'+
              'SIZE \n'+
              'point radius: %s \n' %(self.r)+
              'window size - w: %s h: %s \n' %(self.window_width, self.window_height)+
              '--------------------------\n')
        
        return 'disp the propeties of object "cloud"'
  
    # change self properties
    def __setattr__(self, item, value):
            self.__dict__[item] = value
    
    # scale axis
    def axis(self):      
        self.position = axes.axes(self.qx, 
                                  self.qy, 
                                  self.qz, 
                                  self.center,
                                  self.zoom, 
                                  self.ratio)
    
    # linear scale value    
    def linear(self, mode = 0):       
        # normalise and rescale value
        value = color.linear(self.qi, mode)
        self.color = painting(self.color_bar, 
                              self.face_color, 
                              value, 
                              self.transparent, 
                              len(value))
    
    # adjust scale value
    def imadjust(self, gamma, low_in=0, high_in=1, low_out=0, high_out=1, mode=0):
        # normalise and adjust rescale value
        value = color.imadjust(self.qi, low_in, high_in, low_out, high_out, mode)
        self.color = painting(self.color_bar, 
                              self.face_color, 
                              value, 
                              self.transparent, 
                              len(value))
        
    # log scale
    def logit(self, mode = 0):
        # log and normalise value
        value = color.logit(self.qi, mode)
        self.color = painting(self.color_bar, 
                              self.face_color, 
                              value, 
                              self.transparent, 
                              len(value))
        
    # strech scale
    def strech(self, e = 1, mode = 0):
        # strech value
        value = color.strech(self.qi, e, mode)
        self.color = painting(self.color_bar, 
                              self.face_color, 
                              value, 
                              self.transparent, 
                              len(value))
        
    # gauss transform
    def gausst(self, height, width, center, mode = 0):
        # gausst value
        value = color.gausst(self.qi, height, width, center, mode)
        self.color = painting(self.color_bar, 
                              self.face_color, 
                              value, 
                              self.transparent, 
                              len(value))
    
    # caluculate hist gram
    def hist(self, g = 65535, mode = 0):
        # calculate hist gram
        hist_list = color.hist(self.qi, g, mode)
        return hist_list
        
    # hist equal
    def hist_equal(self, g=65535, mode=0):
        # hist equal scale data
        value = color.hist_equal(self.qi, g, mode)
        self.color = painting(self.color_bar, 
                              self.face_color, 
                              value, 
                              self.transparent, 
                              len(value))
    
    # point it on window
    def scatter(self, mode = 'point'):
        
        #----------------------------------------------------------------------#
        
        # import vertex and fragment shader
        if mode == 'point':
            
            # point mode, no light
            # shader and program
            vertex   = shader.vertex_point      # vertex shader
            fragment = shader.fragment_point    # fragmenet shader
            program  = gloo.Program(vertex, fragment, count=len(self.qi))
                                                # program
        elif mode == 'diffuse':

            # difffuse mode, diffuse light scattering
            # shader and program
            vertex   = shader.vertex_diffuse    # vertex shader
            fragment = shader.fragment_diffuse  # fragmenet shader
            program  = gloo.Program(vertex, fragment, count=len(self.qi))
                                                # program
            program['light'] = self.light       # add light source                                
                
        elif mode == 'specular':

            # difffuse mode, diffuse light scattering
            # shader and program
            vertex   = shader.vertex_specular   # vertex shader
            fragment = shader.fragment_specular # fragmenet shader
            program  = gloo.Program(vertex, fragment, count=len(self.qi))
                                                # program
            program['light'] = self.light       # add light source  
            
        else:
            raise ValueError('This mode has not been developed yet! \n'+
                             'Please choose from point, diffuse and specular.')
        
        #----------------------------------------------------------------------#
        
        # open a window
        back_color = color.RGB1[self.back_color]
        window = app.Window(self.window_width, 
                            self.window_height, 
                            color=(back_color[0],
                                   back_color[1],
                                   back_color[2], 
                                   self.back_alpha))
        # shader variable setting
        program['position']   = self.position                    # position
        program['radius']     = self.r                           # point radius
        program['bg_color']   = self.color                       # point color
        program['model']      = np.eye(4, dtype=np.float32)      
        program['projection'] = np.eye(4, dtype=np.float32)
        program['view']       = glm.translate(np.eye(4, dtype = np.float32), 0, 0, self.translate)

        #----------------------------------------------------------------------#
        
        @window.event

        def on_draw(dt):
        
            window.clear()
            program.draw(gl.GL_POINTS)
            
            # make rotation
            self.theta += self.r_theta
            self.phi   += self.r_phi
            self.chi   += self.r_chi
            
            model = np.eye(4, dtype=np.float32)
            
            #""" -------------------------------------------------------
            #rotate(M, angle, x, y, z, point=None)
            #---------------------------------------------------------"""
            glm.rotate(model, self.theta, 0, 0, 1)
            glm.rotate(model, self.phi,   0, 1, 0)
            glm.rotate(model, self.chi,   1, 0, 0)
            
            program['model'] = model


        #----------------------------------------------------------------------#

        @window.event
            
        def on_resize(width,height):
            program['projection'] = glm.perspective(45.0, width / float(height), 1.0, 1000.0)
        
        gl.glEnable(gl.GL_DEPTH_TEST)
        app.run()

        #-------------------------------------------------------------#
