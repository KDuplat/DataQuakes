#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 13 14:58:39 2022

@author: oramos
"""
import numpy as np
import math

def logbins(dist1,nbins, xmax):
    
    dist2=np.zeros((nbins,2))
    
    nmax=dist1.shape[0]
    
    n=nmax-1
    while n>xmax or dist1[n]==0:
        n=n-1
    nmax=n
    step1=math.log(nmax+1,10)/nbins
    
    for x in range(nbins):
        x1=10**(x*step1);
        x2=10**((x+1)*step1);
        dist2[x,0]=10**((2*x)*step1/2);
        count1=0;
        for k in range(nmax):
           if k>=x1 and k<x2:
               dist2[x,1]=dist2[x,1]+dist1[k];
               count1=count1+1;
        dist2[x,1]=dist2[x,1]/count1
    return dist2        
        
    
    
    
        