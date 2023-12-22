#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 11:37:08 2023

@author: oramos
"""

from leastsquares import leastsquares
from logbins import logbins
from twopoints import twopoints 

import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import gridspec



def mainfct(alpha, ncifras, dim, lenghtTab, filenametab, casetab, nbfile, nbins):
    nalpha=len(alpha)
    
    d1=np.zeros((lenghtTab,nalpha)) 
    for j in range(len(filenametab)):
        readfile(casetab[j], filenametab[j], nalpha, d1, j)
    
    d2=d1.copy()
    
    ext1=np.zeros(nalpha)
    max_ava=np.zeros(nalpha)
    disip=np.zeros(nalpha)

    for i in range (nalpha):
        ext1[i]=lenghtTab-1
    
    
    suma1=np.zeros(nalpha)
    meanvalue1=np.zeros(nalpha)
    meanvalue_calcul=np.zeros(nalpha)
        
    
    for x in range(nalpha):
        disip[x]=100*(1-dim[x]*2*alpha[x]/ncifras[x])
        for y in range(lenghtTab):
            suma1[x]=suma1[x]+d1[y,x] # Compte le nombre total d'avalanche
    
    for x in range(nalpha):
        for y in range(lenghtTab):
            d1[y,x]=d1[y,x]/suma1[x] #Normalise l'histograme
            meanvalue1[x]=meanvalue1[x]+(y+1)*d1[y,x] # Calcule la valeur moyenne des avalaches
    
    ndist=np.zeros((nalpha,nbins, 2))
    ndistloglog=np.zeros((nalpha,nbins,2))
    nstat=np.zeros((4,nalpha))
    ndatafit=np.zeros((nalpha,2,2))
    nmin=np.zeros(nalpha)
    nmax=np.zeros(nalpha)
    
    for i in range (nalpha):
        nmin[i]=1
        nmax[i]=8
        
    for j in range(nalpha):
        ndist [j,:,:]=logbins(d1[:,j],nbins, ext1[j])   # logbins of P(s)    
        
        for x in range(nbins):
            for y in range(2):
                if ndist[j,x,y]==0:
                    ndistloglog[j,x,y]=ndistloglog[j,x-1,y]
                else:
                    ndistloglog[j,x,y]=math.log(ndist[j,x,y],10)
                
        nstat[:,j]=leastsquares(ndistloglog[j,:,:],int (nmin[j]),int (nmax[j]))                #best linear fit
        ndatafit[j,:,:]=twopoints(ndistloglog[j,:,:],int(nmin[j]),int(nmax[j]),nstat[:,j])   #fit line
    
    return ndatafit, ndistloglog, disip, nstat, d2
    
    
def statfct(alpha, ncifras, dim, lenghtTab, filenametab, casetab, nbfile, nbins, tabndata):
    nalpha=len(alpha)
    
    d1=np.zeros((lenghtTab,nalpha)) 
    for j in range(len(filenametab)):
        readfile(casetab[j], filenametab[j], nalpha, d1, j, tabndata[j])
    
    d2=d1.copy()
    
    ext1=np.zeros(nalpha)
    max_ava=np.zeros(nalpha)
    disip=np.zeros(nalpha)

    for i in range (nalpha):
        ext1[i]=lenghtTab-1
    
    
    suma1=np.zeros(nalpha)
    meanvalue1=np.zeros(nalpha)
    meanvalue_calcul=np.zeros(nalpha)
        
    
    for x in range(nalpha):
        disip[x]=100*(1-dim[x]*2*alpha[x]/ncifras[x])
        for y in range(lenghtTab):
            suma1[x]=suma1[x]+d1[y,x] # Compte le nombre total d'avalanche
    
    for x in range(nalpha):
        for y in range(lenghtTab):
            d1[y,x]=d1[y,x]/suma1[x] #Normalise l'histograme
            meanvalue1[x]=meanvalue1[x]+(y+1)*d1[y,x] # Calcule la valeur moyenne des avalaches
    
    ndist=np.zeros((nalpha,nbins, 2))
    ndistloglog=np.zeros((nalpha,nbins,2))
    nstat=np.zeros((4,nalpha))
    ndatafit=np.zeros((nalpha,2,2))
    nmin=np.zeros(nalpha)
    nmax=np.zeros(nalpha)
    
    for i in range (nalpha):
        nmin[i]=1
        nmax[i]=8
        
    for j in range(nalpha):
        ndist [j,:,:]=logbins(d1[:,j],nbins, ext1[j])   # logbins of P(s)    
        
        for x in range(nbins):
            for y in range(2):
                if ndist[j,x,y]==0:
                    ndistloglog[j,x,y]=ndistloglog[j,x-1,y]
                else:
                    ndistloglog[j,x,y]=math.log(ndist[j,x,y],10)
                
        nstat[:,j]=leastsquares(ndistloglog[j,:,:],int (nmin[j]),int (nmax[j]))                #best linear fit
        ndatafit[j,:,:]=twopoints(ndistloglog[j,:,:],int(nmin[j]),int(nmax[j]),nstat[:,j])   #fit line
    
    return ndatafit, ndistloglog, disip, nstat, d2


    
def readfile(case, filename, nalpha, d1, j, ndata=0):
    if case==0:
            avalanche_size=np.loadtxt(filename)[:,1]
            #i=0
            for x in avalanche_size:
                d1[int(x),j]+=1
                #i+=1
    
    if case==1:                 #Data Master
            i=0
            f=open(filename,'r')
            for x in f:
                d1[i,j]=x
                i+=1
    if case==2:             #To only take the stationary state
        avalanche_size=np.loadtxt(filename)[:,1]
        i=0
        for x in avalanche_size:
            if (i>ndata):
                d1[int(x),j]+=1
            i+=1