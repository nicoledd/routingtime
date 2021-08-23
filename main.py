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
    # out0:2*5*10 = 100
        # p = 0, 0.01
        # n = 10, 20, 30, ..., 100
        # samples = 10

pVals = np.arange(0, 0.02, 0.01) # gather data for p = 0, 0.01
pLen = len(pVals)
nVals = [i for i in range(10, 60, 10)] # gather data for n = 10, 20, 30, ... , 100
nLen = len(nVals)
un = pLen*nLen
samples = 10 # try 10 samples of each point
idmod = args.id % un

n = nVals[idmod//pLen]
p = pVals[idmod % pLen]


test(n*n, p)
