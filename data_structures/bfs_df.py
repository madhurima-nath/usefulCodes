# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 11:39:54 2017

@author: madhurima
"""

## This bfs makes subgraph containing certain number of lines for a directed weighted graph. 
## The file is read into a dataframe first. It is easier to do the rest of the manipulations.



import numpy as np
import collections
import random
import pandas as pd


def readg():
    f = open('file.txt','r')
    lines = f.readlines()
    s = [] 
    t = [] 
    w = []
    c = {} 
     
    for l in lines:
        s.append(l.split()[0])
        t.append(l.split()[1])
        w.append(round(float(l.split()[2]),3))
     
    c['s'] = s
    c['t'] = t
    c['w'] = w
    
    cf = pd.DataFrame(c, columns = ['s','t','w'])
    
    f.close()
    return s, cf

def tot_len(lst):
    if type(lst) == list:
        return sum(tot_len(sublst) for sublst in lst)
    else:
        return 1

def bfs(g, start, num):
    visited = set()
    queue = collections.deque(start)
    vs = []
    vt = []
    wt = []
    
    while queue:
        vertex = queue.popleft()
    
        if vertex not in visited:
            visited.add(vertex)
            neighbors = list(g.loc[g['s'] == vertex, 't'])
            w = list(g.loc[g['s'] == vertex, 'w'])
            for neighbor in neighbors:
                queue.append(neighbor)
                   
            vs.append(np.repeat(vertex, len(neighbors)))
            vt.append(neighbors)    
            wt.append(w)
            
        if tot_len(vs) >= num:
            vs.pop(-1)
            vt.pop(-1)
        else:
            vlist = [item for sublist in vs for item in sublist]
            elist = [item for sublist in vt for item in sublist]   
            wlist = [item for sublist in wt for item in sublist]
            
    return vlist, elist, wlist


def subgraph():  
    user_id, dtf = readg()
    start = random.sample(user_id, 1)
    
    sub_source, sub_target, wgt = bfs(dtf, start, 100)   ## you want a subgraph made out of the bfs which has 100 edges
        
    d = {}
    d['susers'] = sub_source
    d['target'] = sub_target
    d['weight'] = wgt
   
    return d

df = pd.DataFrame(subgraph())
df.to_csv('foo.txt', sep = '\t', header = False, index = False, encoding = 'utf-8')

