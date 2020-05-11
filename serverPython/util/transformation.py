# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 18:38:44 2020

@author: Yihao
"""

import numpy as np

def multiply(R1,p1,R2,p2):
    
    R = np.matmul(R1, R2)
    p = np.matmul(R1, p2.reshape((3,1))) + p1.reshape((3,1))
    
    return R, p

def getInverse(R, p):
    
    R = R.T
    p = np.matmul(-R, p.reshape((3,1)))
    
    return R, p

def getHomoVector(p):
    
    return np.append(np.array(p),1)

def getRPFromHomo(T):
    
    R = T[0:3,0:3]
    p = T[0:3,3]
    
    return R, p