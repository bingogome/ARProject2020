# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 16:32:39 2020
The class definition file of the bounding sphere class
@author: Yihao
"""

import numpy as np

class BoundingSphere:
    
    def __init__(self, tri):
        self.triangle = tri
        self.center, self.radius = findQAndR(self.triangle)
    
def findQAndR(tri):
    a = tri.a
    b = tri.b
    c = tri.c
    inequality = checkInequality(a,b,c)
    if inequality:
        center = (a+b)/2
    else:
        f = (a+b)/2
        u = a-f
        v = c-f
        d = np.cross(np.cross(u,v),u)
        gamma = (np.dot(v,v) - np.dot(u,u)) / (2*np.dot(d,v-u))
        if gamma <= 0:
            lam = 0 # lambda
        else:
            lam = gamma
        center = f + lam * d
    radius = np.linalg.norm(center-a)
    return center, radius
    
def checkInequality(a,b,c):
    q = (a+b)/2
    inequality = False
    if np.dot(b-q,b-q) == np.dot(a-q,a-q) \
    and np.dot(c-q,c-q) <= np.dot(a-q,a-q) \
    and np.dot(np.cross(b-a,c-a),q-a) == 0:
        inequality = True
        
    return inequality
    