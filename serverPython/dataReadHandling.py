# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 17:17:15 2020

@author: Yihao
"""

import numpy as np

def convertPlySur(path):
    
    numOfPts = int(np.loadtxt(path, skiprows=4, max_rows=1, usecols=(2)))
    numOfTri = int(np.loadtxt(path, skiprows=8, max_rows=1, usecols=(2)))
    coordinates = np.loadtxt(path,skiprows=11,max_rows=numOfPts,usecols=(0,1,2))
    indices = np.loadtxt(path,skiprows=11+numOfPts,usecols=(1,2,3)).astype(int)

    return coordinates, indices

def readAndTransformModel(path, r, p):
    
    numOfPts = int(np.loadtxt(path,max_rows=1))
    coordinates = np.loadtxt(path,skiprows=1,max_rows=numOfPts)
    numOfTri = int(np.loadtxt(path,skiprows=1+numOfPts,max_rows=1))
#    indices = np.loadtxt(path,skiprows=1+numOfPts+1,usecols=(0,1,2)).astype(int)
    indices = np.loadtxt(path,skiprows=1+numOfPts+1,usecols=(1,2,3)).astype(int)
    
    triangles = np.empty([3*numOfTri, 3])
    
    for i in range(numOfPts):
        coordinates[i] = np.matmul(r, coordinates[i]).reshape((3,)) + p
        
    for i in range(numOfTri):
        
        triangles[3*i] = coordinates[indices[i][0]]
        triangles[3*i+1] = coordinates[indices[i][1]]
        triangles[3*i+2] = coordinates[indices[i][2]]
    
    return triangles

def coordAndIndices2Triangles(coordinates, indices):
    numOfPts = len(coordinates)
    numOfTri = len(indices)
    triangles = np.empty([3*numOfTri, 3])
    
    for i in range(numOfTri):
        
        triangles[3*i] = coordinates[indices[i][0]]
        triangles[3*i+1] = coordinates[indices[i][1]]
        triangles[3*i+2] = coordinates[indices[i][2]]
    
    return triangles

def readMeshFile(path): 
    # this function reads in modified .ply file (no header) - line 1: number of vertices, line 2 - N+1: vertices coordinates, line N+2: number of triangles, rest: triangle indices
#   'data\\skull_vertices.ply'
    numOfPts = int(np.loadtxt(path,max_rows=1))
    coordinates = np.loadtxt(path,skiprows=1,max_rows=numOfPts)
    numOfTri = int(np.loadtxt(path,skiprows=1+numOfPts,max_rows=1))
#    indices = np.loadtxt(path,skiprows=1+numOfPts+1,usecols=(0,1,2)).astype(int)
    indices = np.loadtxt(path,skiprows=1+numOfPts+1,usecols=(1,2,3)).astype(int)
    
    triangles = np.empty([3*numOfTri, 3])
    
    for i in range(numOfTri):
        
        triangles[3*i] = coordinates[indices[i][0]]
        triangles[3*i+1] = coordinates[indices[i][1]]
        triangles[3*i+2] = coordinates[indices[i][2]]
    
    return triangles