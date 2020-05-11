# -*- coding: utf-8 -*-
"""
Created on Thu May  7 18:57:04 2020

@author: Yihao
"""
import numpy as np
import pyvista as pv
from scipy.spatial.transform import Rotation
from util.polarisUtilityScript import toolPivCal
from util.polarisUtilityScript import digitizationRightHand
from dataReadHandling import readAndTransformModel
from dataReadHandling import convertPlySur
from dataReadHandling import coordAndIndices2Triangles
from util.octree.createSphereAndTriangles import createSpheres
from util.octree.BoundingBoxTreeNode import BoundingBoxTreeNode
from util.icp import octreeSearchMatch
import socket
import json
import time

loadCalibratedPointer = True
loadCalibratedHemo = True
loadCalibratedSkull = True
loadCollectedImplant = True
pathMeshFile = 'data/skullRimLeftHand.sur'
quatSkull = np.array([-0.7071068, 0.0000000, 0.0000000, 0.7071068])
posSkull = 1000 * np.array([-0.0330000, -0.0658000, -0.0580000])
quatImplant = np.array([-0.4427488, -0.0442963, 0.1601198, 0.8811204])
posImplant = 1000 * np.array([-0.0209000, 0.0522000, -0.0153000])


# tool rom number: pointer - 2, hemostat - 1, skull reference - 0.

#############################################################################
# 1.0 Calibration of the tools and markers

# 1.1 Pointer tool pivot calibration
if loadCalibratedPointer:
    pCalPointer = np.loadtxt('data/out/pCalPointer.txt')
else:
    pCalPointer, _ = toolPivCal([2], 50, 5) 
    np.savetxt('data/out/pCalPointer.txt',pCalPointer)
# 1.1.1 Convert to left handedness
pCalPointerLeft = -pCalPointer

# 1.2 Hemostat pivot calibration
if loadCalibratedHemo:
    pCalHemo = np.loadtxt('data/out/pCalHemo.txt')
else:
    pCalHemo, _ = toolPivCal([1], 50, 5) 
    np.savetxt('data/out/pCalHemo.txt',pCalHemo)
# 1.2.1 Convert to left handedness
pCalHemoLeft = -pCalHemo

# 1.3 Skull marker pivot calibration
if loadCalibratedSkull:
    pCalSkull = np.loadtxt('data/out/pCalSkull.txt')
else:
    pCalSkull, _ = toolPivCal([0], 50, 5) 
    np.savetxt('data/out/pCalSkull.txt',pCalSkull)
# 1.3.1 Convert to left handedness
pCalSkullLeft = -pCalSkull

#############################################################################
# 2. Model sample collection

# 2.1 Implant model digitization - (should still be in right handedness)
if loadCollectedImplant:
    tImplant = np.loadtxt('data/out/digitizedImplant.txt')
else:
    print('press enter key to collect points on the implant')
    input()
    tImplant = digitizationRightHand(200, 10, pCalHemo, pCalPointer, [1,2]) 
    np.savetxt('data/out/digitizedImplant.txt',tImplant)

# 2.2 Create implant surface
surfImplant = pv.PolyData(tImplant).delaunay_2d()
surfImplant.save('data/implantSurface.ply', binary=False)
implantCoord, implantIndices = convertPlySur('data/implantSurface.ply')


#############################################################################
# 3. Receive a transformation of implant from virtual space (note now both implant and skull should be x-flipped)


rSkull = Rotation.from_quat(quatSkull)
rImplant = Rotation.from_quat(quatImplant)

# 3.1 Load the skull model and transform it to the moved position
print('Data meshing ...')
spheres = createSpheres(readAndTransformModel(pathMeshFile, rSkull.as_matrix(), posSkull))
print('Creating octree ...')
octree = BoundingBoxTreeNode(spheres)
print('Data meshing completed, and octree created.')

# 3.2 Convert the implant model to left handedness (flip x) 
implantCoordLeft = implantCoord
implantCoordLeft[:,0] = -implantCoordLeft[:,0] 


# 3.3 Transform implant model to the moved position
for i in range(implantCoordLeft.shape[0]):
    implantCoordLeft[i] = np.matmul(rImplant.as_matrix(), implantCoordLeft[i].reshape((3,1))).reshape((3,))+posImplant

# 3.4 Match the points to the surface and calculate distance
print('start searching ...')
cOut, dist = octreeSearchMatch(implantCoordLeft, octree)

#############################################################################
# 4. Send heat map data and the point pair on the skull

# unity /1000
implantCoordLeftSend = implantCoordLeft/1000
implantIndicesSend = implantIndices.reshape(-1)
# convert distance into 0~1 range
distColor = (dist-min(dist))/(max(dist)-min(dist))

udpIP = 'localhost'
udpPort = 8051
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = json.dumps({'GetImplantMesh': {'vertices': implantCoordLeftSend.reshape(-1).tolist(), 'triangles': implantIndicesSend.tolist(), 'color': distColor.tolist()}})
# message = json.dumps({'GetImplantMesh': {'vertices': (0.1*np.array([[0,0.3,0],[0,0,1],[1,0.5,0],[1,0.5,1],[2,0.5,1],[3,0.5,3]])).reshape(-1).tolist(), 'triangles': [0,1,2,1,3,2,2,3,4,3,4,5], 'color': [0.1,1,0.3,1]}})
for i in range(3000):
    sock.sendto(message.encode('utf-8'), (udpIP, udpPort))
    time.sleep(5)
sock.close()

#############################################################################















