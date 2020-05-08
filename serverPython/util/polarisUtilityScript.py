# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 18:01:20 2020

Grader please note: this script is custimized from the script of my CISII project

@author: Yihao
"""

import time
import six
import numpy as np
from sksurgerynditracker.nditracker import NDITracker

def initAndCollect(romNum, numOfSamples, collectionFreq):
    
    #    The reason why we collection all three frames has to do with the library
    #    scikit-surgeryndutrakcer. Initially, when feed in 3 rom files, it gives
    #    an UnicodeError. After editting the library source code, it works for 3 rom files
    #    but gives error for 1 rom file.
    
    settings_polaris = {"tracker type": "polaris",
        "romfiles" : ["share/roms/SD.960-315.rom", "share/roms/CarbonFiberFiducial.rom", "share/roms/SD.960-553.rom"]}
    
    tracker = NDITracker(settings_polaris)
    print('Start point collection procedure.')
    tracker.start_tracking()
    dataAcquired = []
    six.print_(tracker.get_tool_descriptions())
    counter = 0
    try:
        while True:
            print('Sample number',counter)
            port_handles, _, framenumbers, tracking, quality = tracker.get_frame()
            print(tracking)

            tracking_ = np.empty([4, 0])
            for i in romNum:
                tracking_ = np.concatenate((tracking_, tracking[i]), axis = 1)
            if not np.isnan(np.sum(tracking_)):
                dataAcquired.append(tracking_)
                counter = counter + 1
            time.sleep(1/collectionFreq)
            if counter == numOfSamples:
                break
    except:
        tracker.stop_tracking()
        tracker.close()
        print('Point collection failed.')
    finally:
        tracker.stop_tracking()
        tracker.close()
        print('Point collection succeed.')
        
    return dataAcquired


def toolPivCal(romNum, numOfSamples, collectionFreq):
    
    dataAcquired = initAndCollect(romNum, numOfSamples, collectionFreq)
    R_IMtraix = np.empty([3*len(dataAcquired),6])
    tVector = np.empty([3*len(dataAcquired),1])
    
    for i in range(len(dataAcquired)):
        R_IMtraix[3*i:3*(i+1),0:3] = dataAcquired[i][0:3,0:3]
        R_IMtraix[3*i:3*(i+1),3:6] = -np.identity(3)
        
        tVector[3*i:3*(i+1),0] = -dataAcquired[i][0:3,3]
        
    tVector_ = np.reshape(tVector,(3*len(dataAcquired),))
    pVector,_,_,_ = np.linalg.lstsq(R_IMtraix, tVector_,rcond=None)
    
    pCal = pVector[0:3]
    pPiv = pVector[3:6]
    
    return pCal, pPiv


def digitizationLeftHand(numOfSamples, collectionFreq, pCalHemo, pCalPointer, romNum):
    # returns the sample points on the implant wrt origin of calibrated hemostat (or any other tool to be origin)
    
    dataAcquired = initAndCollect(romNum, numOfSamples, collectionFreq)
 
#    Initialize data collection holder 
    t = np.empty([len(dataAcquired),3])
    
    pCalHemo = np.append(np.array(pCalHemo),1) # homogeneous form of the calibrated p
    pCalPointer = np.append(np.array(pCalPointer),1) # homogeneous form of the calibrated p
    
    for i in range(len(dataAcquired)):
        
        # conduct transformation
        RHemo = dataAcquired[i][0:3,0:3]
        
        THemo = dataAcquired[i][:,0:4]
        THemo[0:3,3] = -THemo[0:3,3] # Switch handedness
        TPointer = dataAcquired[i][:,4:8]
        TPointer[0:3,3] = -TPointer[0:3,3] # Switch handedness
        
        pHemoPrime = np.matmul(THemo, pCalHemo)
        pPointerPrime = np.matmul(TPointer, pCalPointer)
        
        THemoPrime = np.zeros((4,4))
        THemoPrime[0:3,0:3] = RHemo
        THemoPrime[:,3] = pHemoPrime
        
        t[i,:] = np.matmul(np.linalg.inv(THemoPrime),pPointerPrime)[0:3]
        
    return t

def digitizationRightHand(numOfSamples, collectionFreq, pCalHemo, pCalPointer, romNum):
    # returns the sample points on the implant wrt origin of calibrated hemostat (or any other tool to be origin)
    
    dataAcquired = initAndCollect(romNum, numOfSamples, collectionFreq)
 
#    Initialize data collection holder 
    t = np.empty([len(dataAcquired),3])
    
    pCalHemo = np.append(np.array(pCalHemo),1) # homogeneous form of the calibrated p
    pCalPointer = np.append(np.array(pCalPointer),1) # homogeneous form of the calibrated p
    
    for i in range(len(dataAcquired)):
        
        # conduct transformation
        RHemo = dataAcquired[i][0:3,0:3]
        
        THemo = dataAcquired[i][:,0:4]
        TPointer = dataAcquired[i][:,4:8]
        
        pHemoPrime = np.matmul(THemo, pCalHemo)
        pPointerPrime = np.matmul(TPointer, pCalPointer)
        
        THemoPrime = np.zeros((4,4))
        THemoPrime[0:3,0:3] = RHemo
        THemoPrime[:,3] = pHemoPrime
        
        t[i,:] = np.matmul(np.linalg.inv(THemoPrime),pPointerPrime)[0:3]
        
    return t












