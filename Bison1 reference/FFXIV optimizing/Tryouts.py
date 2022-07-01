import math
import vlc
import time
import sys
import os
import itertools

def GCD(sks):
    k = 1900/130
    mults_of_k = math.floor((sks - 400)/k)
    print(mults_of_k)

    if mults_of_k < 1:
        GCD = 2.50
    elif mults_of_k == 1:
        GCD = 2.50 - 0.01
    elif mults_of_k > 1:
        m = math.floor((mults_of_k - 1) / 4)
        GCD = 2.49 - 0.01 * m

    return round(GCD, 2)

def fGCD(CD, sks):
    CD = CD * 1000
    GCD = math.floor(CD * (1000 + math.ceil(130 * (400 - sks)/ 1900)) / 10000) / 100 
    return GCD


def fSpeed(sks):
    fSPD = math.floor(130 * (sks - 400) / 1900 + 1000)
    return fSPD

def fCriticalHit(CRIT):
    fCRIT = math.floor(200 * (CRIT - 400)/1900 + 1400)
    return fCRIT

#Generate all combinations of input scope
def GenerateCombinations(scope, floorLim):
    srange = []
    for k in scope:
        srange.append(list(range(floorLim, k + 1)))
    Combinations = list(itertools.product(*srange))
    return Combinations

MateriaSet = GenerateCombinations([7, 7], 1)

for mat in MateriaSet:
    print(mat)


