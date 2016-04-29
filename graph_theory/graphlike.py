'''
Created on Apr 13, 2016

This is a base class to understand graphs in the computational sense.
It attempts to maintain the more abstract properties and "description" of 
mathematical graphs as a collection of two objects (in this case, two 
mutable collections), one of vertices, and edges. A third representation
implementing both is also used: adj -- the adjacency matrix, a dictionary
whose keys are the [vertex1,vertex2] ordered pair, and whose entries vary
depending on the implementation of Graphlike, but defaults to 0 when
no edge exists from vertex1 to vertex2.


This abstract class is designed to provide an abstract base class (ABC) 
for the entirety of the graphlike objects included in this package:
graph, digraph, multigraph, psuedograph, psuedo

@author: unoriginalbanter
'''
from abc import ABCMeta, abstractmethod, abstractproperty

class Graphlike(object):
    '''
    abstract class, cannot instantiate it as a standalone instance
    '''
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def __init__(self):
        '''
        Constructor
        '''
        self.vertices = None
        self.edges = None
        self.adj = None
        
    def set_vertices(self, vertices):
        self.vertices = vertices
        
    def get_vertices(self):
        return self.vertices
    
    def set_edges(self, edges):
        self.edges = edges
        
    def get_edges(self):
        return self.edges

    def set_adj(self, adj_m):
        self.adj = adj_m
        
    def get_adj(self):
        return self.adj
    
    abstractproperty(get_vertices, set_vertices)
    abstractproperty(get_edges, set_edges)
    abstractproperty(get_adj, set_adj)
    
    @abstractmethod 
    def add_vertex(self, vertex):
        '''Adds a vertex to the graphlike object's vertices and adj 
        properties.
        '''
        pass
    
    @abstractmethod 
    def add_edge(self, edge):
        '''Adds an edge to the graphlike object's edges and adj properties.'''
        pass
    
    @abstractmethod 
    def is_legal(self):
        '''Checks if the graphlike object is contextually legal for its type.
        IE., strict graphs cannot have a weighted edge value other than 1 or 
        0, while weighted_graphs can.'''
        pass
    
    