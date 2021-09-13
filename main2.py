import os
import networkx as nx
import argparse




def getGeo(filename):
    G = nx.Graph()
    with open(filename) as file:
        while (line := file.readline().rstrip()):
            edge = line.split()
            G.add_edge(int(edge[0]), int(edge[1]))
    file.close()
    x = len(G)
    
    H = max(nx.connected_components(G), key=len)
    y = nx.average_shortest_path_length(H)

    return x, y


# n = side length
# p = node defect probability
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-id', type=int, required=True) # make this 1 arg
args = parser.parse_args()


files = ['./facebook100txt/UCSB37.txt', './facebook100txt/Wake73.txt', './facebook100txt/Wesleyan43.txt', './facebook100txt/Auburn71.txt', './facebook100txt/Princeton12.txt', './facebook100txt/USFCA72.txt', './facebook100txt/Cal65.txt', './facebook100txt/UC61.txt', './facebook100txt/UC64.txt', './facebook100txt/Rutgers89.txt', './facebook100txt/Haverford76.txt', './facebook100txt/Carnegie49.txt', './facebook100txt/Mississippi66.txt', './facebook100txt/Vanderbilt48.txt', './facebook100txt/Santa74.txt', './facebook100txt/JMU79.txt', './facebook100txt/UPenn7.txt', './facebook100txt/UNC28.txt', './facebook100txt/NYU9.txt', './facebook100txt/Brown11.txt', './facebook100txt/USF51.txt', './facebook100txt/Brandeis99.txt', './facebook100txt/USC35.txt', './facebook100txt/Lehigh96.txt', './facebook100txt/Columbia2.txt']



x, y = getGeo(files[args.id])
print(x, y)