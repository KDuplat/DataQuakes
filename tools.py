#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 15:44:14 2023

@author: Kilian
"""

import numpy as np

def avg(tab, nbfile, nbdisip):
    avg=np.zeros((nbdisip, len(tab[0])))
    x=0
    for i in range(len(tab)):
        if (x==nbdisip):
            x=0
        for j in range (len(tab[i])):
            avg[x,j]+=tab[i, j]/nbfile
        x+=1
    
    return avg


def stdev (tab, nbfile, nbdisip, tabmoy):
    stddev=np.zeros((nbdisip,len(tab[0])))
    
    x=0

    for i in range(len(tab)):
        if (x== nbdisip):
            x=0
        for j in range(len(tab[0])):
            stddev[x,j]+=(tab[i,j]-tabmoy[x,j])**2
        x+=1

    stddev=(stddev/nbfile)**(1/2)
    
    return stddev