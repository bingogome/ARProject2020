# -*- coding: utf-8 -*-
"""
Created on Mon May 11 17:48:39 2020

@author: Yihao
"""

import time
import socket
import json
import numpy as np
import pyvista as pv
from dataReadHandling import convertPlySur
from util.polarisUtilityScript import digitizationLeftHand
from util.point2point import point2point
from util.transformation import multiply

def highLightSkullArea(loadCollectedSkullHighLight, pCalSkullLeft, pCalPointerLeft, rSkull, posSkull, udpIP):
    if loadCollectedSkullHighLight:
        tSkull = np.loadtxt('data/out/digitizedSkull.txt')
    else:
        print('press enter key to collect points on the skull')
        input()
        tSkull = digitizationLeftHand(200, 10, pCalSkullLeft, pCalPointerLeft, [0,2]) 
        np.savetxt('data/out/digitizedSkull.txt',tSkull)
    
    surfSkullArea = pv.PolyData(tSkull).delaunay_2d()
    surfSkullArea.save('data/skullAreaSurfaceLeft.ply', binary=False)
    skullCoord, skullIndices = convertPlySur('data/skullAreaSurfaceLeft.ply')
    
    collectedFiducials = np.loadtxt('data/out/collectedSkullFiducialsLeftHand.txt')
    modelFiducials = np.array([[62.2834,-101.639,137.095],\
                                [71.8019,-134.585,176.091],\
                                [1.41721,-44.5984,153.749],\
                                [1.14525,-60.4037,191.706],\
                                [1.32943,-175.998,211.543],\
                                [-59.9893,-109.185,171.305],\
                                [-53.9599,-117.288,120.412]]) # From front to back, from right to left. (the last 2 pointes (left) are from upper to lower)
    RInit, pInit = point2point(collectedFiducials, modelFiducials)
    
    skullAreaRot, skullAreaPos = multiply(rSkull,posSkull,RInit,pInit);
    
    for i in range(skullCoord.shape[0]):
        skullCoord[i] = np.matmul(skullAreaRot, skullCoord[i].reshape((3,1))).reshape((3,))+skullAreaPos.reshape(-1)
    
    skullCoordSend = skullCoord/1000
    skullIndicesSend = skullIndices.reshape(-1)
    
    udpPort2 = 8053
    sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # note "GetImplantMesh" does not only work for implant. It's just a json block name. Did not want to change it
    
    messageSkullArea = json.dumps({'GetImplantMesh': {'vertices': skullCoordSend.reshape(-1).tolist(), 'triangles': skullIndicesSend.tolist(), 'color': [0.5]*len(skullCoordSend)}})
    
    print('start sending ...')
    for i in range(3000):
        sock2.sendto(messageSkullArea.encode('utf-8'), (udpIP, udpPort2))
        time.sleep(5)
    soc2.close()