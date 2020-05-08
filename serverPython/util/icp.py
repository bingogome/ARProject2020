# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 21:07:26 2020

@author: Yihao

Description: Performs Iterative Closest Point to register point cloud to
             coordinate system of surface mesh 
Inputs:  d, 
         octree              The proper data structure 
Outputs: R and p, optimal transformation for
         Body Coordinates --> CT registration

"""

import numpy as np
from util.point2point import point2point

def icp(d, octree, RInit, pInit, iterationMax, saveResult):
    
    # Initialize algorithm parameters
    error = np.full(d.shape, float('inf'))
    epsilonBar = float('inf')
    # rotReg = np.identity(3)
    # pReg = np.zeros(3)
    rotReg = RInit
    pReg = pInit
    s = np.zeros(d.shape) # Registered coordinates
    
    gamma = 0.95
    threshold = 3 * epsilonBar        
    
    n = 1
    convergeCount = 0
    
    while (convergeCount < 10 and iterationMax==-1) or ((not iterationMax == -1) and n<=iterationMax):
        print('ICP interation:', n)
        
        # update s
        for i in range(len(s)):
            s[i] = np.matmul(rotReg, d[i]) + pReg
            
        cOut, errOut = octreeSearchMatch(s, octree)
        
        # delete the ones that are larger than the threshold
        distances = errOut
        deletMask = distances <= threshold
        cOutCut = cOut[deletMask, ...]
        dCut = d[deletMask, ...]
        
        # Find the best transformation
        rReg, pReg = point2point(dCut, cOutCut)
        if saveResult == True and n%5 == 0:
            np.savetxt('data/out/rReg.txt',rReg)
            np.savetxt('data/out/pReg.txt',pReg)
        
        print('Actual number of samples:', cOut.shape[0])
        print('Number of samples used for registration:', cOutCut.shape[0])
        sCut = np.zeros(cOutCut.shape)
        
        # register d using the calculated transformation
        for i in range(sCut.shape[0]):
            sCut[i] = np.matmul(rotReg, dCut[i]) + pReg
    
        # Calculate discrepancy
        error = cOutCut - sCut
        epsilonBarOld = epsilonBar
        epsilonBar = getEpsBar(error)
        epsilonBarRatio = epsilonBar / epsilonBarOld
        threshold = 3 * epsilonBar
        
        # count convergence history
        print(epsilonBarRatio)
        if gamma <= epsilonBarRatio and epsilonBarRatio <= 1.000:
            convergeCount = convergeCount + 1
            print('converge count:',convergeCount,'Goal: 10')
        else:
            convergeCount = 0
        
        n = n+1
        
    return rReg, pReg

def getEpsBar(error):
    dotProduct = np.zeros((error.shape[0],))
    for i in range(error.shape[0]):
        dotProduct[i] = np.dot(error[i],error[i])
    
    numerator = sum(np.sqrt(dotProduct))
    result = numerator / error.shape[0]
    return result

def octreeSearchMatch(s, octree):
    cOut = np.empty(s.shape)
    errOut = np.empty(s.shape[0])
    for i in range(len(s)):
        bound = float('inf')
        closest = np.array([float('inf'),float('inf'),float('inf')])
        v = s[i]
        v,bound,closest = octree.findClosestPoint(v,bound,closest)
        cOut[i] = closest
        errOut[i] = bound
    return cOut, errOut