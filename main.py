import networkx as nx
import numpy.core.multiarray
import numpy as np
import random
import math
import argparse
import csv
import algorithm
from algorithm import Grid, Algorithm

# performs 1 test
def test(n, p):
    grid = Grid(n,p)
    algorithm = Algorithm(grid.G, n, grid.m)
    print("number of nodes,p,routing time,number of nodes after defects")
    print(n, ",", p, ",", algorithm.time, ",", algorithm.m) # prints routing time and size of grid
    return algorithm.time, algorithm.m



# n = side length
# p = node defect probability
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-id', type=int, required=True) # make this 1 arg
args = parser.parse_args()



# total number of jobs is pLen * nLen * samples
    # out0:2*10*10 = 200
        # p = 0, 0.01
        # n = 10, 20, 30, ..., 100
        # samples = 10
    # out1: 9*10*10 = 900
        # p = 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1
        # n = 10, 20, 30, ..., 100
        # samples = 10
    # out2: 10*10*10 = 1000
        # p = 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2
        # n = 10...100 in increments of 10
        # samples = 10
    # out3: 21*10*90
        # p = 0...0.2 in increments 0.01
        # n = 10...100 in increments of 10
        # samples = 90

    # change 1. pVals and 2. arrays and 3. out directory (in bashscript.sh)

pVals = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2] # gather data for p = various values
pLen = len(pVals)
nVals = [i for i in range(10, 110, 10)] # gather data for n = 10, 20, 30, ... , 100
nLen = len(nVals)
un = pLen*nLen
samples = 90
idmod = args.id % un

n = nVals[idmod//pLen]
p = pVals[idmod % pLen]


test(n*n, p)
