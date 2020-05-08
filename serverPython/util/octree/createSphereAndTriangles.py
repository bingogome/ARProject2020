# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 18:18:18 2020

@author: Yihao
"""

from util.octree.boundingSphere.BoundingSphere import BoundingSphere
from util.octree.boundingSphere.Triangle import Triangle

def createSpheres(tris):
    spheres = []
    triangles = createTriangles(tris)
    for i in triangles:
        spheres.append(BoundingSphere(i))
    return spheres

def createTriangles(tri):
    tris = []
    for i in range(tri.shape[0]):
        if i%3 == 0:
            tris.append(Triangle(tri[i:i+3]))
    return tris