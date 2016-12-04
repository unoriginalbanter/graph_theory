"""
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
"""
from abc import ABCMeta, abstractmethod, abstractproperty


class Graphlike(object):
    """
    abstract class, cannot instantiate it as a standalone instance
    """
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def __init__(self):
        """
        Constructor
        """
        self._vertices = None
        self._edges = None
        self._adjacency_matrix = None

    @property
    @abstractproperty
    def vertices(self):
        return self._vertices

    @vertices.setter
    @abstractproperty
    def vertices(self, vertices):
        self._vertices = vertices

    @property
    @abstractproperty
    def edges(self):
        return self._edges

    @edges.setter
    @abstractproperty
    def edges(self, edges):
        self._edges = edges

    @property
    @abstractproperty
    def adjacency_matrix(self):
        return self._adjacency_matrix

    @adjacency_matrix.setter
    @abstractproperty
    def adjacency_matrix(self, matrix):
        self._adjacency_matrix = matrix

    @abstractmethod
    def add_vertex(self, vertex):
        """Adds a vertex to the graphlike object's vertices and adjacency_matrix
        properties.
        """
        pass
    
    @abstractmethod 
    def add_edge(self, edge):
        """Adds an edge to the graphlike object's edges and adjacency_matrix properties."""
        pass
    
    @abstractmethod
    def is_edge(self, v1, v2):
        """Returns true if v1, v2 is an edge."""
        pass
    
    @abstractmethod
    def is_an_edge(self, v1, *vertices):
        """Returns the first edge encountered from v1 to any of the vertices,
        but if not, returns False."""
        pass
    
    @abstractmethod
    def adjacent(self, vertex):
        """Returns a collection of vertices that are adjacent to vertex."""
        pass
    
    @abstractmethod
    def other_vertices(self, *vertices):
        """Returns the collection of other vertices, distinct from vertex."""
        pass