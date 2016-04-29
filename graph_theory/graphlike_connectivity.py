'''
Created on Apr 19, 2016

@author: unoriginalbanter

This module contains methods that operate on various graphlike objects to find
values related to mathematic connectivity within graphs, including distance
searches, paths, cycles, minimum weight trees, etc. For proper implementation,
see each method.
'''
from . import graphlike, graph

def complete_graph(n):
    '''
    Creates and returns a complete graph of order n, K_n.
    The vertices created are named with integers from 0 to n for ease
    of navigation. Though, this distinction is arbitrary in complete graphs.
    '''
    K = graph.Graph()
    for i in range(n):
        K.add_vertex(i)
        K.add_edges({v,i} for v in K.get_vertices(), v!=i)
    return K 

def is_complete_graph(graph):
    '''
    Returns true if given graph is a complete graph, false else.
    Checks adjacency matrix for nonzero entries, so, returns true if the edges 
    exist even in directed and weighted graphs.
    '''
    for edge, val in graph.get_adj():
        
        
        

def breadth_first_distance(graphlike_object, vertex):
    '''
    Performs the basic distance algorithm, Breadth-First Distance.
    For the given vertex, returns a dictionary of distances for each other
    vertex u1,u2,...,uN of your Graphlike object.
    '''
    