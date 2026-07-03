# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 13:20:41 2016

@author: madhurima
"""

import pandas as pd


def mapnodes_weight(file):
    ''' This function maps the node ids (either integers
        or strings) which may or may not be continous to integers
        starting from 0. Input file is in edgelist format with 
        first column as the source, second column the target 
        and the third one the edge weight.
    '''
    fn = open(file, 'r')
    lines = fn.readlines()
    
    l1 = []
    l2 = []
    l3 = []
    
    for line in lines:
        l = line.split()
        l1.append(l[0])
        l2.append(l[1])
        l3.append(l[2])
    
    c = {}
    
    c['s'] = l1
    c['t'] = l2
    c['w'] = l3
    
    cf = pd.DataFrame(c)
    
    cf[['s', 't']] = pd.Series(cf[['s', 't']].stack().factorize()[0], index = cf[['s', 't']].stack().index).unstack()
    ##this will change only the 's' and 't' column keeping the third column unchanged
    
    cf.to_csv('foo.txt', sep = '\t', header = False, index = False, encoding = 'utf-8')
    ## put the path along with the filename, if required. This will form the file 'foo.txt' in the same directory as file.txt.
    
    fn.close()
    

def mapnodes(file):
    ''' This function maps the node ids (either integers
        or strings) which may or may not be continous to integers
        starting from 0. Input file is in edgelist format with 
        first column as the source, second column the target.
    '''
    fn = open(file, 'r')
    lines = fn.readlines()
    
    l1 = []
    l2 = []
    
    for line in lines:
        l = line.split()
        l1.append(l[0])
        l2.append(l[1])
    
    c = {}
    
    c['s'] = l1
    c['t'] = l2
    
    cf = pd.DataFrame(c)
    
    cf = pd.Series(cf.stack().factorize()[0], index = cf.stack().index).unstack()
    
    cf.to_csv('foo.txt', sep = '\t', header = False, index = False, encoding = 'utf-8')
    ## put the path along with the filename, if required. This will form the file 'foo.txt' in the same directory as file.txt.
    
    fn.close()

mapnodes('file.txt')
mapnodes_weight('file.txt')
