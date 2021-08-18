import algorithm
from algorithm import Grid, Algorithm
import networkx as nx
import numpy as np
import random
import math
import argparse
import csv


# performs 1 test
def test(n, p):
    grid = Grid(n,p)
    algorithm = Algorithm(grid.G, n, grid.m)
    print(algorithm.time, algorithm.m) # prints routing time and size of grid
    return algorithm.time, algorithm.m



# n = side length
# p = node defect probability
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-n', type=int, required=True) # make this 1 arg
parser.add_argument('-p', type=float, required=True) # make this 1 arg
args = parser.parse_args()


test(args.n, args.p)
