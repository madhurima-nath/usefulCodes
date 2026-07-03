# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 13:01:34 2016

@author: madhurima
"""

from collections import deque
import networkx as nx
import random
import pandas as pd
import numpy as np


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


def comp(source, visited, num):
    '''
    This generates lists containing the sources as the nodes
    from the visited list after BFS and the targets as the 
    corresponding neighbors. The 'num' gives the maximum 
    number of unique nodes that would be present in the list
    of the source nodes. If all the nodes are required, delete
    the 'maxlen' entry.    
    '''
    vs = deque([], maxlen = num)
    vt = []
    vslist = []

    for i in range(len(visited)):
        if visited[i] in source:
            j = source.index(visited[i])
            vs.append(source[j])
    ## from the list of the visited nodes, find those which 
    ## are in the source list of the original graph
    
    for j in range(len(vs)):
        vt.append(g.neighbors(vs[j]))
        vslist.append(list(np.repeat(vs[j], len(g.neighbors(vs[j])))))
    ## find the corresponding target nodes for the source nodes
    
    vlist = [item for sublist in vslist for item in sublist]
    elist = [item for sublist in vt for item in sublist] 
    
    return vlist, elist


def subgraph():  
    '''
    This generates a subgraph using the source and the target
    nodes obtained from the previous function
    '''
    snodes = readgraph()
    start = random.sample(snodes, 1)
    node_visited = bfs(g, start)
    
    sub_source, sub_target = comp(snodes, node_visited, 3)
    
    
    ## uncomment the following if there is a graph that has edge weight
    ## and the final subgraphs require this edge weight values
    
#    wgt = []
#    for l in range(g.number_of_edges()):
#        for i,j in zip(sub_source, sub_target):
#            if (i,j) == g.edges()[l]:
#                wgt.append(g.edges(data = True)[l][2]['weight'])
    
    d = {}
    d['susers'] = sub_source
    d['target'] = sub_target
#    d['weight'] = wgt
   
    return d

df = pd.DataFrame(subgraph())
df.to_csv('sg.txt', sep = '\t', header = False, index = False, encoding = 'utf-8')




