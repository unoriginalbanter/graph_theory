'''
Created on Apr 19, 2016

@author: unoriginalbanter

This module contains methods that operate on various graphlike objects to find
values related to mathematic connectivity within graphs, including distance
searches, paths, cycles, minimum weight trees, etc. For proper implementation,
see each method.
'''
from objects import graphlike
from objects import graph

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
    adjacency = graph.get_adj()
    for key in adjacency.keys():
        if adjacency[key]==None:
            return False
    return True
        
def is_graphical_sequence(sequence):
    """
    Returns true if parameter sequence is a graphical sequence (a sequence that
    can describe the degree of the vertices of a graph).
    """
    seq = [integer for integer in sequence.sort(reverse=True)]
    p = len(seq)
    for d in seq:
        if d >= p-1:
            #if there is an integer d that is d>=(p=1), is not graphical
            return False
        elif d < 0:
            #if there is a negative integer in sequence, then it is not graphical
            return False
    if (d == 0 for d in seq):
        #if all terms are zero, then the sequence is graphical
        return True
    #ELSE: remove the first (largest) term d1, and subtract 1 from next d1 terms 
    first_term = seq.pop(0)
    for i in range(first_term):
        seq[i] = seq[i] - 1
    #ELSE (cont): repeat
    is_graphical_sequence(seq)

def breadth_first_distance(graphlike_object, vertex):
    '''
    Performs the basic distance algorithm, Breadth-First Distance.
    For the given vertex, returns a dictionary of distances for each other
    vertex u1,u2,...,uN of your Graphlike object.
    '''
    distances = {vertex:0}
    distance = 1
    others = graphlike_object.other_vertices(vertex)
    for other in others:
        if graphlike_object.is_edge(vertex, other):
            distances[other] = distance
            others.remove(other)
        
    