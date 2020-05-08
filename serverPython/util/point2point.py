# -*- coding: utf-8 -*-
"""
Refered to Matlab codes from Authors: Yihao Liu & Timothy Bernard
Description: Performs Rigid 3D Points registration to minimize difference 
              between two points of clouds 
Inputs:  Reference Point Set (n,3)
         Observed Point Set (n,3)

Outputs: R and p, optimal transformation for point set registration
Method due to K. Arun, et. al., IEEE PAMI, Vol 9, no 5, pp 698-700, Sept 1987

"""

import numpy as np

def point2point(ptCloudA, ptCloudB):
    
    n = np.shape(ptCloudA)[0]
    
    centPtCloudA = (1/n) * sum(ptCloudA)
    centPtCloudB = (1/n) * sum(ptCloudB)
    
    # Point Deviation from centroid
    ptDevA = ptCloudA - centPtCloudA
    ptDevB = ptCloudB - centPtCloudB
    
    H = np.zeros((3,3))
    
    for i in range(n):
        H = H + np.matmul(ptDevA[i].reshape((3,1)),  ptDevB[i].reshape((1,3)))
    
    U, S, V = np.linalg.svd(H)
    
    # Rotation
    R = np.matmul(V.T, U.T)
    
    p = centPtCloudB - np.matmul(R, centPtCloudA)
    
    return R, p