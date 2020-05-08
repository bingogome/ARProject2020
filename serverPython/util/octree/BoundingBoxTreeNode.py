# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 19:05:56 2020

@author: Yihao
"""

import numpy as np
from util.octree.boundingSphere.Triangle import findClosestPointTriangle

class BoundingBoxTreeNode:
    
    def __init__(self, spheres):
        self.spheres = spheres
        self.haveSubtrees = False
        self.nS = len(self.spheres)
        self.cent = getCentroid(self.spheres)
        self.maxRadius = getMaxRadius(self.spheres)
        self.upBound, self.lowBound = getBounds(self.spheres)
        self.constructSubtrees()
        
    def constructSubtrees(self):
        minCount = 16 # user defined min count of tree node
        minDiag = 10.0 # user defined minimum diagnol distance
        if self.nS <= minCount \
        or np.linalg.norm(self.upBound-self.lowBound) <= minDiag:
            self.haveSubtrees = False
            return
        
        self.haveSubtrees = True
        self.subtrees = [BoundingBoxTreeNode([]) for count in range(8)]
        indexArray = self.splitSort()
        cur = 0
        for numOfSp, i in zip(indexArray, [0,1,2,3,4,5,6,7]):
            self.subtrees[i] = BoundingBoxTreeNode(self.spheres[cur:cur+numOfSp])
            cur+=numOfSp
#        self.spheres = [] # to save memory
        
    def splitSort(self):
        nnn = 0; npn = 0; npp = 0; nnp = 0; 
        pnn = 0; ppn = 0; ppp = 0; pnp = 0;
        sphereArrayTemp = [[],[],[],[],[],[],[],[]]
        for i in range(self.nS):
            if (self.spheres[i].center < self.cent).tolist() == [1,1,1]:
                nnn+=1
                sphereArrayTemp[0].append(self.spheres[i])
            elif (self.spheres[i].center < self.cent).tolist() == [1,0,1]:
                npn+=1
                sphereArrayTemp[1].append(self.spheres[i])
            elif (self.spheres[i].center < self.cent).tolist() == [1,0,0]:
                npp+=1
                sphereArrayTemp[2].append(self.spheres[i])
            elif (self.spheres[i].center < self.cent).tolist() == [1,1,0]:
                nnp+=1
                sphereArrayTemp[3].append(self.spheres[i])
            elif (self.spheres[i].center < self.cent).tolist() == [0,1,1]:
                pnn+=1
                sphereArrayTemp[4].append(self.spheres[i])
            elif (self.spheres[i].center < self.cent).tolist() == [0,0,1]:
                ppn+=1
                sphereArrayTemp[5].append(self.spheres[i])
            elif (self.spheres[i].center < self.cent).tolist() == [0,0,0]:
                ppp+=1
                sphereArrayTemp[6].append(self.spheres[i])
            elif (self.spheres[i].center < self.cent).tolist() == [0,1,0]:
                pnp+=1
                sphereArrayTemp[7].append(self.spheres[i])
        self.spheres = [dummyInner for dummyOuter in sphereArrayTemp for dummyInner in dummyOuter]
                
        return [nnn,npn,npp,nnp,pnn,ppn,ppp,pnp]
       
    def findClosestPoint(self, v, bound, closest):
        dist = bound + self.maxRadius
        if (v>self.upBound+dist).tolist() != [[0,0,0]]:
            return v,bound,closest
        if (v<self.lowBound-dist).tolist() != [[0,0,0]]:
            return v,bound,closest
        if self.haveSubtrees == 1:
            for i in self.subtrees:
                v,bound,closest = i.findClosestPoint(v,bound,closest)
        else:
            if self.nS>0:
                for i in self.spheres:
                    v,bound,closest = updateClosest(i,v,bound,closest)
        return v,bound,closest
        
def getCentroid(spheres):
    summation = np.zeros((3))
    for i in range(len(spheres)):
        summation = summation + spheres[i].center
    if len(spheres) == 0:
        return np.array([float('-inf'),float('-inf'),float('-inf')])
    cent = summation/len(spheres)
    return cent

def getMaxRadius(spheres):
    rMax = 0
    for i in spheres:
        r = i.radius
        rMax = max(rMax,r)
    return rMax

def getBounds(spheres):
    upBound = np.array([[float('-inf'),float('-inf'),float('-inf')]])
    lowBound = np.array([[float('inf'),float('inf'),float('inf')]])
    for i in spheres:
        t = i.triangle
        tri = np.concatenate((t.a, t.b, t.c))
        tri = tri.reshape((3,3))
        compare1 = np.concatenate((tri,upBound), axis=0)
        compare2 = np.concatenate((tri,lowBound), axis=0)
        upBound = np.amax(compare1, axis=0).reshape((1,3))
        lowBound = np.amin(compare2, axis=0).reshape((1,3))
    return upBound, lowBound

def updateClosest(sphere,v,bound,closest):
    dist = np.linalg.norm(v-sphere.center)
    if dist-sphere.radius > bound:
        return v,bound,closest
    cp = findClosestPointTriangle(v,sphere.triangle)
    dist = np.linalg.norm(cp-v)
    if dist<bound:
        bound = dist
        closest = cp
    return v,bound,closest


    