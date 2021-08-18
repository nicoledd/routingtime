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
#parser.add_argument('-p', type=float, required=True) # make this 1 arg
args = parser.parse_args()


pVals = np.arange(0, 0.02, 0.01) # change to increments of 0.01 later
pLen = len(pVals)
nVals = [i for i in range(5, 20, 5)] # change to 100 later
nLen = len(nVals)
un = pLen*nLen
samples = 2

idmod = args.id % un

n = nVals[idmod//pLen]
p = pVals[idmod % pLen]


test(n*n, p)
