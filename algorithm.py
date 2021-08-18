import networkx as nx
import numpy as np
import random
import math
import grid
from grid import Grid

class Algorithm:
    
    def __init__(self, G, n, m, debug=False):
        self.debug = debug # do we print the debug statements or not
        self.G = G # networkx graph object
        self.n = n # number of nodes in G if it were non-defective
        self.m = m # actual number of nodes in G
        self.tokens()
        self.swaps = self.routing(self.G) # function to do routing
        self.time = len(self.swaps) # routing time
    
    
    
    def tokens(self):
        tokens = list(self.G)
        random.shuffle(tokens)
        nodes = list(self.G)
        for i in range(len(self.G)):
            self.G.nodes[nodes[i]]['token'] = tokens[i]
    
    
    
    
    # h: a subgraph of grid.G to be divided and routed
    def routing(self, h):
        
        swaps = []

        if(h.number_of_nodes() == 1): # base case: for a graph of size 1, do nothing
            return []
        
        U,V = self.divide(h) # divide input graph into 2 subgraphs
        
        U, V = self.classify(U), self.classify(V)   # classify tokens as proper or improper
        
        if self.improper(U) > 0:  # if there exist improper tokens, use max flow and osmosis
            flow = self.capacity(U, V)
            swaps = self.osmosis(U, V, flow)

        U_swaps = self.routing(U) # recur for both subgraphs
        V_swaps = self.routing(V)

        uv_max = max(len(U_swaps), len(V_swaps)) # combine swaps since they occur in parallel
        while len(U_swaps) < uv_max:
            U_swaps.append([])
        while len(V_swaps) < uv_max:
            V_swaps.append([])
        for u_op,v_op in zip(U_swaps, V_swaps):
            combined_op = u_op+v_op
            swaps.append(combined_op)
        
        return swaps
    
        
        
        
        
    # step 1: divides graph into 2 halves based on the nodes farthest away from each other
    # farthest() finds nodes u, v farthest away from each other
    # bfs() performs bfs on u, v
    # subtree() forms subtrees that start from u, v
    # color() displays divide using color map
    def divide(self, H):
        u, v = self.farthest(H)
        U_nodes, V_nodes = self.subtree(H, u, v)
        U = self.G.subgraph(U_nodes)
        V = self.G.subgraph(V_nodes)
        return U,V
    
    def farthest(self, h):
        distances = dict(nx.all_pairs_shortest_path_length(h))
        m = 0
        u = 0
        v = 0
        for src, src_dists in distances.items():
            for sink, d in src_dists.items():
                if(d >= m):
                    u = src
                    v = sink
                    m = d
        return u, v
    def bfs(self, H, u, v):
        u_bfs = nx.shortest_path_length(H, source=u)
        u_bfs = {int(k):int(v) for k,v in u_bfs.items()}
        v_bfs = nx.shortest_path_length(H, source=v)
        v_bfs = {int(k):int(v) for k,v in v_bfs.items()}
        return u_bfs, v_bfs
    def subtree(self, H, u, v):
        u_bfs, v_bfs = self.bfs(H, u, v)
        U_nodes = []
        V_nodes = []
        equals = []
        for i in range(H.number_of_nodes()):
            n = list(H)[i]
            if(u_bfs[n] < v_bfs[n]):
                U_nodes.append(n)
            elif(u_bfs[n] > v_bfs[n]):
                V_nodes.append(n)
            else:
                equals.append(n)
        if(len(U_nodes) > len(V_nodes)):
            U_nodes += equals
        else:
            V_nodes += equals
        return U_nodes, V_nodes
    def color(self, U_nodes, V_nodes):
        color_map = []
        for a in list(self.G):
            if a in U_nodes:
                color_map.append('red')
            elif a in V_nodes:
                color_map.append('green')
        self.display(color_map)
        
        
        
        
        
        
        
    # step 2: classifys each token as proper or improper
    def classify(self, U):
        for u in U.nodes():
            if U.nodes[u]['token'] in list(U):
                U.nodes[u]['properness'] = "proper"
            else:
                U.nodes[u]['properness'] = "improper"
        return U
    
    
    
    
    
    
    # step 3: finds flow
    def capacity(self, U, V):
        D = self.directed(U, V)
        num_improper = self.improper(U)

        
        # exponential search code
        high = 1
        f, flow = self.findflow(D, high)  # does a capcaity of 1 work?
        if(f == num_improper):
            return flow
        
        low = 0 # prev value of k that doesn't work
        while(f != num_improper):
            low = high
            high *= 2
            f, flow = self.findflow(D, high)
        high, flow = self.binary(D, low+1, high, num_improper, flow)   # perform binary search between (l, k]
        f, flow = self.findflow(D, high)
        if f != num_improper:
            raise Exception(f"ew {f} {num_improper}")
                
        return flow # use dictionary to route tokens
        
        
    # useful helper function
    def findflow(self, D, k):
        for a,b in D.edges():
            if(a != 's' and b != 'd'):
                D[a][b]['capacity'] = k
        f, flow = nx.maximum_flow(D, 's', 'd')
        return f, flow
    

    # exponential search function
    def binary(self, D, low, high, num_improper, flow):
        if low == high:
            return low, flow
        mid = (low + high) // 2
        f, flow = self.findflow(D, mid)
        if f != num_improper:
            return self.binary(D, mid+1, high, num_improper, flow)
        else:
            return self.binary(D, low, mid, num_improper, flow)
        
        
    # make boundary edges directed
    def directed(self, U, V):
        
        D = self.G.subgraph(list(U) + list(V)).to_directed() # form directed subgraph of G using nodes of U, V
        D.add_node('s')   # add source and sink nodes
        D.add_node('d')
        
        for u in U.nodes():  # connect s to U's improper tokens
            if(U.nodes[u]['properness'] == 'improper'):
                D.add_edge('s', u, capacity = 1)
                
        for v in V.nodes():  # connect d to V's improper tokens
            if(V.nodes[v]['properness'] == 'improper'):
                D.add_edge(v, 'd', capacity = 1)
                
        # remove boundary edges that go from V to U
        B = self.boundary_edges(U, V)
        for u,v in B:
            D.remove_edge(v, u)
        
        return D
    
    def improper(self, U):
        num_improper = 0
        for u in U.nodes():
            if(U.nodes[u]['properness'] == 'improper'):
                num_improper += 1
        return num_improper

  
    def dprint(self, *args, **kwargs):
        if self.debug: print(*args, **kwargs)


            
            


    # step 4: osmosis ################
    def osmosis(self, U, V, flow):
        swaps = []
        U,V = self.distances(U,V)
        odd_U, even_U = self.oddeven(U)
        odd_V, even_V = self.oddeven(V)
        b = self.boundary_edges(U, V)
        num = 0
        num_improper = self.improper(U)
        self.dprint('num_improper:',num_improper)
        self.dprint("oddevens: ",odd_U,even_U,odd_V,even_V)
        while(num != num_improper):
            self.dprint('num:',num, '\n')
            self.dprint('nodes:', self.G.nodes(data=True), '\n')
            self.dprint('flow: ',flow)
            
            # arrays to store swaps
            odd_swaps = []
            boundary_swaps = []
            even_swaps = []
            
            # get boundary swaps between U and V
            boundary_swaps += self.boundaryswaps(b, U, V, flow)
            num += len(boundary_swaps)
            
            # get odd swaps in both U and V
            sw, flow = self.getswaps(U, odd_U, 's', flow)
            odd_swaps += sw
            sw, flow = self.getswaps(V, odd_V, 'd', flow)
            odd_swaps += sw
            
            # perform boundary swaps and odd swaps
            self.doswaps(boundary_swaps, True)
            self.doswaps(odd_swaps, False)
            odd_swaps += boundary_swaps
            
            # get even swaps in both U and V
            sw, flow = self.getswaps(U, even_U, 's', flow)
            even_swaps += sw
            sw, flow = self.getswaps(V, even_V, 'd', flow)
            self.dprint('flow (after):', flow)
            even_swaps += sw
            
            # perform even swaps
            self.doswaps(even_swaps, False)
            
            # keep track of which swaps we've performed so far
            if odd_swaps:
                swaps.append(odd_swaps)
            if even_swaps:
                swaps.append(even_swaps)
            
            self.dprint("SWAPS:",odd_swaps, even_swaps)
        
        return swaps
    
    
    
    
    # perform all token swaps, if it's a boundary swap then make sure to mark both tokens as proper now
    def doswaps(self, swaps, b):
        for u, v in swaps:
            self.G.nodes[u]['token'], self.G.nodes[v]['token'] = self.G.nodes[v]['token'], self.G.nodes[u]['token']
            if(b == True):
                self.G.nodes[u]['properness'] = 'proper'
                self.G.nodes[v]['properness'] = 'proper'
            else:
                self.G.nodes[u]['properness'], self.G.nodes[v]['properness'] = self.G.nodes[v]['properness'], self.G.nodes[u]['properness']
            
            
    def boundaryswaps(self, b, U, V, flow):
        swaps = []
        dests = []
        for u, v in b:
            # if both are improper, swap them
            if(U.nodes[u]['properness'] == 'improper' and V.nodes[v]['properness'] == 'improper'
               and u not in dests and v not in dests
               and flow[u][v] > 0):
                swaps.append((u, v))
                dests.append(u)
                dests.append(v)
                flow[u][v] -= 1
        return swaps
    

    def oddeven(self, H):
        odd = []
        even = []
        for u,v in H.edges():
            if(H.nodes[u]['distance'] < H.nodes[v]['distance']):
                w = u
            else:
                w = v
            if(H.nodes[w]['distance'] % 2 == 1):
                odd.append((u, v))
            else:
                even.append((u, v))
        return odd, even
    
    def getswaps(self, H, indices, s, flow):
        swaps = []
        dests = []
        for u,v in indices:
            if s == 's' and flow[u][v] == 0:
                u,v = v,u
            if s == 's':
                uflow,vflow = u,v
            if s == 'd' and flow[v][u] == 0:
                u,v = v,u
            if s == 'd':
                uflow, vflow = v,u
            if(H.nodes[u]['properness'] == 'improper' and H.nodes[v]['properness'] == 'proper'
               and flow[uflow][vflow] > 0
               and u not in dests and v not in dests):
                swaps.append((u, v))
                flow[uflow][vflow] -= 1 # decrement flow
                dests.append(v)
                dests.append(u)
        return swaps, flow
    
        
        
        
    def boundary_edges(self, U, V):
        b = []
        for u in U.nodes():
            for v in self.G.neighbors(u):
                if v in list(V):
                    b.append((u,v))
        return b
    
        
        
                           
    # returns boundary nodes and edges of U and V
    def boundary(self, U, V):
        U_boundary = []
        V_boundary = []
        for u in U.nodes():
            for v in self.G.neighbors(u):
                if v in list(V):
                    U_boundary.append(u)
                    V_boundary.append(v)
        return set(U_boundary), set(V_boundary)
    
    # calculates indices/distances
    def distances(self, U, V):
        U_boundary, V_boundary = self.boundary(U, V)
        U_dists = nx.multi_source_dijkstra_path_length(U, U_boundary)
        V_dists = nx.multi_source_dijkstra_path_length(V, V_boundary)
        for u in U.nodes():
            U.nodes[u]['distance'] = U_dists[u]
        for v in V.nodes():
            V.nodes[v]['distance'] = V_dists[v]
        return U, V
    
    
    
    
    
    
    
    # step 0: displays the graph G ############
    def display(self, color_map):
        pos = self.positions()
        plt.figure(1,figsize=(20,20))
        nx.draw(self.G, pos, node_color=color_map, with_labels=True, node_size=300)
        plt.show()
        
    def positions(self):
        s = math.sqrt(self.n)
        pos = {0:(0,0)}
        count = 0
        y = 0
        for v in range(self.n):
            count += 1
            if count % s == 1 and v != 0:
                y += 1
            pos[v] = (int(v % s), -y)
        return pos