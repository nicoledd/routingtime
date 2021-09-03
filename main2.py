import networkx as nx
import numpy.core.multiarray
import numpy as np
import random
import math
import argparse
import csv
import algorithm


def getData(filename):
    G = nx.Graph()
    with open(filename) as file:
        while (line := file.readline().rstrip()):
            edge = line.split()
            G.add_edge(int(edge[0]), int(edge[1]))
    file.close()
    
    # find largest component and its diameter
    cc = max(nx.connected_components(G), key=len)
    largestCC = G.subgraph(list(cc))
    diam = nx.algorithms.distance_measures.diameter(largestCC)
    
    # find distance between all pairs of vertices
    dists = nx.algorithms.shortest_paths.unweighted.all_pairs_shortest_path_length(largestCC)
    result = dict(dists)
    sumOfDists = 0
    num = 0
    for k,v in result.items():
        for k2,v2 in v.items():
            sumOfDists += v2
            num += 1
    avgDist = sumOfDists/num
    
    print("diameter of largest component, network size, avg dist between vertices, size of largest component")
    print(diam, ",", len(G), ",", avgDist, ",", len(largestCC))


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-id', type=int, required=True)
args = parser.parse_args()


filenames = ['Haverford76.txt', 'Harvard1.txt', 'Princeton12.txt', 'UC64.txt', 'Middlebury45.txt', 'William77.txt', 'Vermont70.txt', 'Northwestern25.txt', 'Northeastern19.txt', 'Dartmouth6.txt', 'Yale4.txt', 'Bucknell39.txt', 'UVA16.txt', 'Notre Dame57.txt', 'Columbia2.txt', 'Virginia63.txt', 'Swarthmore42.txt', 'WashU32.txt', 'Rochester38.txt', 'Berkeley13.txt', 'UNC28.txt', 'Bingham82.txt', 'Vanderbilt48.txt', 'USC35.txt', 'USF51.txt', 'GWU54.txt', 'Carnegie49.txt', 'Tennessee95.txt', 'NYU9.txt', 'UCLA26.txt', 'Villanova62.txt', 'Cal65.txt', 'UC61.txt', 'UIllinois20.txt', 'UChicago30.txt', 'USFCA72.txt', 'MIT8.txt', 'UConn91.txt', 'Rutgers89.txt', 'Oklahoma97.txt', 'Indiana69.txt', 'Howard90.txt', 'UCF52.txt', 'UGA50.txt', 'Auburn71.txt', 'FSU53.txt', 'BU10.txt', 'Brown11.txt', 'Michigan23.txt', 'Temple83.txt', 'Colgate88.txt', 'Simmons81.txt', 'MSU24.txt', 'MU78.txt', 'Maine59.txt', 'Cornell5.txt', 'American75.txt', 'Oberlin44.txt', 'Hamilton46.txt', 'Caltech36.txt', 'Smith60.txt', 'Rice31.txt', 'UC33.txt', 'Wesleyan43.txt', 'UCSC68.txt', 'Wake73.txt', 'Pepperdine86.txt', 'Duke14.txt', 'Amherst41.txt', 'UCSB37.txt', 'Williams40.txt', 'Mississippi66.txt', 'Mich67.txt', 'UPenn7.txt', 'Tufts18.txt', 'Vassar85.txt', 'UCSD34.txt', 'Maryland58.txt', 'Penn94.txt', 'Bowdoin47.txt', 'UMass92.txt', 'Baylor93.txt', 'UF21.txt', 'Texas80.txt', 'Stanford3.txt', 'Wisconsin87.txt', 'Emory27.txt', 'Brandeis99.txt', 'BC17.txt', 'Georgetown15.txt', 'Trinity100.txt', 'Johns Hopkins55.txt', 'Syracuse56.txt', 'Tulane29.txt', 'Lehigh96.txt', 'Reed98.txt', 'Santa74.txt', 'JMU79.txt', 'Wellesley22.txt', 'Texas84.txt']
getData(filenames[args.id])