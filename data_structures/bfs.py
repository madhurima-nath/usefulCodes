# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 12:06:42 2016

@author: madhurima
"""

from collections import deque
import networkx as nx
import random

def readgraph():
    ''' This reads the input graph file as edgelist with the
        first column as the source nodes and the second column
        as the target nodes. Default is undirected graphs.
        
        To read directed graphs, use the following in the 
        read_edgelist function:
            read_edgelist('file.txt', create_using=nx.DiGraph())
        To read directed graphs and with edge weights or any other
        data for the edges, use:
            read_edgelist('file.txt',  create_using=nx.DiGraph(),
                data=(('weight',float),), edgetype=float)
    '''
    global g
    g = nx.read_edgelist('file.txt',  create_using=nx.DiGraph(),
                         data=(('weight',float),), edgetype=float)
    
    source = []
    target = []
    
    for i in range(g.number_of_edges()):
         source.append(g.edges(data = True)[i][0])
         target.append(g.edges(data = True)[i][1])
    return source


def bfs(graph, start):
    '''
    This searches the graph. It starts with a random node and
    searches for it's neighbors. Only if the neighbor is not
    visited it is added to the list. It returns a list
    containing the nodes which as attached to the starting node
    and the ones attached to the neighbors of the starting node.
    '''    
    visited = []
    queue = deque(start)
    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            visited.append(vertex)
            neighbors = graph.neighbors(vertex)
            
            for neighbor in neighbors:
                queue.append(neighbor)
    return visited

snodes = readgraph()
start = random.sample(snodes, 1)
node_visited = bfs(g, start)

def writetofile(nlist):
    '''
    This allows to write the list containing the nodes from the 
    BFS into a file. 
    '''
    with open('node_list_bfs.txt', 'w', encoding = 'utf-8') as fn:
        for lines in nlist:
            fn.write(lines+'\n')

writetofile(node_visited)
