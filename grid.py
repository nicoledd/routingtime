import networkx as nx
import numpy as np
import random
import math

class Grid:
    
    # n: the grid will be sqrt(n) x sqrt(n)
    # p: each node on the grid will have a probability p of not existing
    def __init__(self, n, p):
        self.n = n
        self.p = p
        self.G = self.constructGrid()
        self.removeNodes()
        self.G = self.largest()
        self.m = len(self.G)
    
    # constructGrid: returns G, a networkx grid graph with 'n' nodes and dimensions sqrt(n) x sqrt(n)
    # assignNodes: returns V, an array [0, 1, ..., n - 1]
    # assignEdges: returns E, an array consisting of edges for a grid graph with 'n' nodes
    # removeNodes: removes nodes with probability 'p'
    def constructGrid(self):
        G = nx.Graph()
        G.add_nodes_from(self.assignNodes())
        G.add_edges_from(self.assignEdges())
        return G
    def assignNodes(self):
        V = []
        for v in range(self.n):
            V.append(v)
        return V
    def assignEdges(self):
        E = []
        s = math.sqrt(self.n)
        """ 1. do not add any edges to node n - 1
         2. if node v is on the right side of the grid, only add a DOWN edge
         3. if node v is on the lower side of the grid, only add a RIGHT edge
         4. otherwise, add a RIGHT edge and a DOWN edge to node v """
        for v in range(self.n):
            if v == self.n - 1:
                pass
            elif v > self.n - s - 1 and v < self.n - 1:
                E.append((v, v + 1))
            elif v % s == s - 1 and v != 0:
                E.append((v, v + s))
            else:
                E.append((v, v + 1))
                E.append((v, v + s))
        return E
    def removeNodes(self):
        for v in range(self.n):
            if(random.uniform(0,1) < self.p):
                self.G.remove_node(v)

    # displays the graph G
    def displayGraph(self):

        # assign coordinate positions to each node in 'G'
        # p[v] = (x,y) implies that node v is at position (x,y)
        pos = self.assignPos()
        
        # draw and display graph 'G'
        plt.figure(1,figsize=(20,20))
        nx.draw(self.G, pos, node_size=1)
        plt.show()
        
        
    # pos: a dictionary where pos[v] = (x,y) implies that the position of node v is (x, y) in a grid graph
    # if the node doesn't exist, don't bother with adding it to the dictionary
    def assignPos(self):
        s = math.sqrt(self.n)
        pos = {0:(0,0)}
        count = 0
        y = 0
        for v in range(self.n):
            count += 1
            if count % s == 1 and v != 0:
                y += 1
            pos[v] = (int(v % s), -y)
        
        # remove all the positions for nodes that don't exist
        for v in range(self.n):
            if v not in self.G.nodes:
                del pos[v]
        return pos
                
    # displays histogram of G's connected component sizes
    def largest(self):
        # generate a sorted list of connected components, largest first
        cc = sorted(nx.connected_components(self.G), key=len, reverse=True)
        return self.G.subgraph(cc[0])