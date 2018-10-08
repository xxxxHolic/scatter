#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 23:16:47 2018

@author: user
"""

##############################################################

#"""
#uniform variable
#
#    /*  uniform变量是外部程序传递给（vertex和fragment）shader的变量。因此它是application通过
#        函数glUniform**（）函数赋值的。在（vertex和fragment）shader程序内部，uniform变量就像
#        是C语言里面的常量（const ），它不能被shader程序修改。（shader只能用，不能改）
#        
#        如果uniform变量在vertex和fragment两者之间声明方式完全一样，则它可以在vertex和fragment
#        共享使用。（相当于一个被vertex和fragment shader共享的全局变量）
#        
#        uniform变量一般用来表示：变换矩阵，材质，光照参数和颜色等信息。
#        
#        以下是例子：
#        
#        uniform mat4 viewProjMatrix;    投影+视图矩阵
#        uniform mat4 viewMatrix;        视图矩阵
#        uniform vec3 lightPosition;     光源位置  */
#"""
#
#"""
#atttribute variable
#
#    /*  attribute变量是只能在vertex shader中使用的变量。（它不能在fragment shader中声明
#        attribute变量，也不能被fragment shader中使用）
#        
#        一般用attribute变量来表示一些顶点的数据，如：顶点坐标，法线，纹理坐标，顶点颜色等。
#        
#        在application中，一般用函数glBindAttribLocation（）来绑定每个attribute变量的位置，
#        然后用函数glVertexAttribPointer（）为每个attribute变量赋值。
#        
#        以下是例子：
#        
#        attribute vec4 position;
#        attribute vec2 texCoord; */
#        
#"""
#"""
#varying variable
#
#    /*  varying变量的作用是从顶点着色器向片元着色器传值，varying变量只能是float类型的，只
#        要在片元着色器中也声明同名varying变量，顶点着色器赋给该变量的值就会自动传入片元着色
#        器（在给片元着色器中的同名varying变量赋值之前，有内插的过程，1.0传过去不一定是1.0）
#        
#        注意：顶点着色器中的varying变量值不是直接传递，会先进行内插，内插就像补间动画一样
#        
#        内插（interpolate）
#        
#        插值，缺少数据才需要插值，比如想要把一系列散点连成平滑曲线，相邻已知点之间缺少很多点，
#        此时就需要通过内插填补缺少的数据，最终平滑曲线上除已知点之外的所有点都是插值得到的
#        
#        例如: Photoshop的自定义渐变，我们只需要设置几个点的颜色就能自动生成一整条渐变带，这
#        几个点之间的颜色都是通过内置插值算法得到的
#        
#        varying变量的值传递到片元着色器之前进行的插值过程被称为内插，同样，我们也可以利用内插
#        生成渐变
#        
#        attribute vec4 color => declare vextexes colors
#        varying vec4 v_color => declare varying variables
#        v_color = color      => set value for varying color  */
#
#"""

#############################VERTEX SHADER##################################

vertex_point =  """
                    uniform mat4 model;               //maps from an object's local coordinate space inot world space
                    uniform mat4 view;                //maps from world space to camera space
                    uniform mat4 projection;          //maps from camera to screen space
                    
                    attribute vec4  bg_color;         //The fragment color
                    attribute vec3  position;         //attribute declare the position of points. without alpha--vec3
                    
                    attribute float radius;
                    
                    varying float v_pointsize;
                    varying float v_radius;
                    
                    varying vec4  v_bg_color;
                    varying vec4  v_position;
                    
                    void main (void)
                        {
                            v_radius = radius;        //varying constant Assignment
                            v_position = projection *view *model *vec4(position, 1.0); 
                                                      //The position of points.
                                                      // 4x4 matrix operating: projection view model
                            v_bg_color = bg_color;
                            
                            gl_Position = v_position;
                            gl_PointSize = 2 *v_radius;
                                                      //The size of points. diameter = 2*radius
                        }
                     
                 """

vertex_diffuse = """
                    uniform mat4 model;               //maps from an object's local coordinate space inot world space
                    uniform mat4 view;                //maps from world space to camera space
                    uniform mat4 projection;          //maps from camera to screen space
                    
                    uniform vec3 light;                //light poosition
                    
                    attribute vec4  bg_color;         //The fragment color
                    attribute vec3  position;         //attribute declare the position of points. without alpha--vec3
                    
                    attribute float radius;
                    
                    varying float v_pointsize;
                    varying float v_radius;
                    
                    varying vec4  v_bg_color;
                    varying vec4  v_position;
                    varying vec3  v_light;
                    
                    void main (void)
                        {
                            v_radius   = radius;      //varying constant Assignment
                            v_position = projection *view *model *vec4(position, 1.0); 
                                                      //The position of points.
                                                      // 4x4 matrix operating: projection view model
                            v_bg_color = bg_color;
                            v_light = light;          //light position
                            
                            gl_Position = v_position;
                            gl_PointSize = 2 *v_radius;
                                                      //The size of points. diameter = 2*radius
                        }
                     
                 """

vertex_specular = """
                    uniform mat4 model;               //maps from an object's local coordinate space inot world space
                    uniform mat4 view;                //maps from world space to camera space
                    uniform mat4 projection;          //maps from camera to screen space
                    
                    uniform vec3 light;               //light poosition
                    
                    attribute vec4  bg_color;         //The fragment color
                    attribute vec3  position;         //attribute declare the position of points. without alpha--vec3
                    
                    attribute float radius;
                    
                    varying float v_pointsize;
                    varying float v_radius;
                    
                    varying vec4  v_bg_color;
                    varying vec4  v_position;
                    varying vec3  v_light;
                    
                    void main (void)
                        {
                            v_radius   = radius;      //varying constant Assignment
                            v_position = projection *view *model *vec4(position, 1.0); 
                                                      //The position of points.
                                                      // 4x4 matrix operating: projection view model
                            v_bg_color = bg_color;
                            v_light = light;          //light position
                            
                            gl_Position = v_position;
                            gl_PointSize = 2 *v_radius;
                                                      //The size of points. diameter = 2*radius
                        }
                     
                 """ 
#############################FRAGMENT SHADER################################## 
        
fragment_point = """
            
                    varying float v_radius;        //point radius
                    
                    varying vec4  v_position;      //point positions
                    varying vec4  v_bg_color;      //face color
                    
                    void main()
                    {
                        float r = v_radius;        //point size (radius)
                          
                        float signed_distance = length(gl_PointCoord.xy - vec2(0.5,0.5))*2*r - v_radius;
                        float border_distance = abs(signed_distance);    
                        float alpha           = border_distance;
                        
                        alpha = exp(-alpha*alpha);
                        
                        gl_FragDepth = 0.1*v_position.z;
                        
                        if(signed_distance < 0) {gl_FragColor = v_bg_color;}
                        else                    {discard;}            
                    }
              
                 """ 
           
fragment_diffuse = """
            
                    varying float v_radius;        //point radius
                    
                    varying vec3  v_light;         //light position
                    varying vec4  v_position;      //point positions
                    varying vec4  v_bg_color;      //face color
                    
                    void main()
                    {
                        float r = v_radius;        //point size (radius)
                          
                        float signed_distance = length(gl_PointCoord.xy - vec2(0.5,0.5))*2*r - v_radius;
                        float border_distance = abs(signed_distance);    
                        float alpha           = border_distance;
                        
                        alpha = exp(-alpha*alpha);
                        
                        gl_FragDepth = 0.1*v_position.z;
                        
                        // add depth color depend on normal and directions
                        
                        vec3  colors    = vec3(v_bg_color.r, v_bg_color.g, v_bg_color.b);
                        vec3  normal    = normalize(vec3(v_position.xy, v_position.z));
                        vec3  direction = normalize(v_light);
                        
                        // add diffuse diffuse scatter effect
                        
                        float diffuse   = max(0.0, dot(direction, normal));
                        
                        if(signed_distance < 0) {gl_FragColor = vec4(diffuse*colors, v_bg_color.a);}
                        else                    {discard;}            
                    }
            
                 """ 
                 
fragment_specular = """
            
                    varying float v_radius;        //point radius
                    
                    varying vec3  v_light;         //light position
                    varying vec4  v_position;      //point positions
                    varying vec4  v_bg_color;      //face color
                    
                    void main()
                    {
                        float r = v_radius;        //point size (radius)
                          
                        float signed_distance = length(gl_PointCoord.xy - vec2(0.5,0.5))*2*r - v_radius;
                        float border_distance = abs(signed_distance);    
                        float alpha           = border_distance;
                        
                        alpha = exp(-alpha*alpha);
                        
                        // add depth color depend on normal and directions
                        
                        gl_FragDepth = 0.1*v_position.z;
                        
                        vec3  colors    = vec3(v_bg_color.r, v_bg_color.g, v_bg_color.b);
                        vec3  normal    = normalize(vec3(v_position.xy, v_position.z));
                        vec3  direction = normalize(v_light);
                        
                        // add diffuse diffuse scatter effect
                        
                        float diffuse   = max(0.0, dot(direction, normal));
                        float specular  = pow(diffuse, 24.0);
                        
                        if(signed_distance < 0) {gl_FragColor = vec4(max(diffuse*colors, specular*vec3(1.0)), v_bg_color.a);}
                        else                    {discard;}            
                    }
            
                 """ 