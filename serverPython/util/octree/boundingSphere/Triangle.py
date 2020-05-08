# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 18:06:14 2020
The class definition file of the bounding triangle class
@author: Yihao

"""

import numpy as np

class Triangle:
    
    def __init__(self, tri):
        self.a, self.b, self.c = findLongestEdge(tri)
    
def findLongestEdge(tri):
    ab = np.linalg.norm(tri[0]-tri[1])
    bc = np.linalg.norm(tri[1]-tri[2])
    ca = np.linalg.norm(tri[2]-tri[1])
    maxEdge = max(ab,bc,ca)
    if maxEdge == ab:
        a = tri[0]
        b = tri[1]
        c = tri[2]
    elif maxEdge == bc:
        a = tri[1]
        b = tri[2]
        c = tri[0]
    elif maxEdge == ca:
        a = tri[2]
        b = tri[0]
        c = tri[1]
    return a,b,c

# using geometry method to find the closest point on the triangle
def findClosestPointTriangle(v, triangle):
    g = (v - triangle.a)
    A = np.array([triangle.b - triangle.a, triangle.c - triangle.a])
    lambdaMu = np.linalg.lstsq(A.T, g, rcond=None)[0]
    c = triangle.a + lambdaMu[0] * (triangle.b - triangle.a) + lambdaMu[1] * (triangle.c - triangle.a)
    
    # if outside of the triangle, get the projected c
    if not (lambdaMu[0]>=0 and lambdaMu[1]>=0 and sum(lambdaMu) <= 1):
        if lambdaMu[0] < 0:
            c = projectOnSegment(c, triangle.c, triangle.a)
        elif lambdaMu[1] < 0:
            c = projectOnSegment(c, triangle.a, triangle.b)
        elif sum(lambdaMu) > 1:
            c = projectOnSegment(c, triangle.b, triangle.c)
    return c
    
def projectOnSegment(c, p, q):
    oldLam = np.dot(c-p,q-p) / np.dot(q-p,q-p)
    lam = max(0, min(oldLam,1))
    c = p+lam * (q-p)
    return c