#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 23:03:32 2018

@author: kaitlynnsnyder
"""

import numpy as np
import matplotlib.pyplot as plt
import random

def runTumble(N,dt):
    
    x = np.empty(N)
    y = np.empty(N)
    
    theta = 0.0
    
    step =  dt
    
    x[0] = 0.0
    y[0] = 0.0
    
    for i in range(1,N):
        
        r = 0.3
        var = random.random()
        
        if var < r:
            theta = 2*np.pi*random.random()
        
        x[i] = x[i-1]+ step*np.cos(theta)
        y[i] = y[i-1]+ step*np.sin(theta)
      

    plt.figure()
    plt.plot(x,y)
    plt.show()
    
    return x,y 
    
def plotSingleParticle():     

    # Total time.
    T = 100.0
    # Number of steps.
    N = 1000000
    # Time step size
    dt = T/N

    # Initial values of x.
    x,y = runTumble(N,dt)
    
    fig = plt.figure(figsize = (12,5))
    
    fig.add_subplot(1,2,1)
    # Plot the 2D trajectory.
    plt.plot(x,y,'b')
    
    
    # Mark the start and end points.
    plt.plot(x[0],y[0], 'go')
    plt.plot(x[-1], y[-1], 'ro')
    
    # More plot decorations.
    plt.title('2D Run-and-Tumble Motion',fontsize=14)
    plt.xlabel('x', fontsize=10)
    plt.ylabel('y', fontsize=10)
    plt.axis('equal')
    plt.grid(True)
    
    distance = np.sqrt(x**2+y**2)
    fig.add_subplot(1,2,2)
    
    steps = np.arange(0,N)
    plt.plot(steps,distance,'r')
    plt.title('RMS Displacement after ' +str(N)+' Steps',fontsize=14)
    plt.xlabel('Number of steps', fontsize=10)
    plt.ylabel('Displacement', fontsize=10)
    

    plt.show()
 
plotSingleParticle()       
