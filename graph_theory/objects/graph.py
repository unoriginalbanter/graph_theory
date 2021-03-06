"""
Created on Apr 13, 2016

@author: unoriginalbanter

This is a base class to understand graphs in the computational sense.
It attempts to maintain the more abstract properties and "description" of 
mathematical graphs as a collection of two objects (in this case, two 
mutable collections), one of vertices (labeled here numerically), and edges 
(a collection of two-tuples whose elements are drawn from the vertices.)
Using this basic description, we can generate a graph, and later implement
extensions of the graph!

We also allow a graph to be tracked and analyzed by its adjacency matrix.
We'll note that we distinguish graphs from digraphs in that 
a graph is any digraph where for any edge in the graph, [v1, v2], 
we have [v2, v1] also an edge. We'll denote this in Python by having our
edges each be sets instead of lists.
"""
import math

from graph_theory.objects import digraph


class Graph(digraph.Digraph):
    """
    Main properties:
        vertices: The nodes of a graph
        edges: The edges between vertices, a collection of pairs (in this case, a set of 2-sets whose entries are
            vertices)
        Adjacency matrix: a two-degree list whose keys are list-pairs of vertices and whose values are 1, or None if no
            edge is present; employs the dictionary representation of a matrix
    """
    def __init__(self, vertices=None, edges=None, adjacency_matrix=None):
        """
        Constructor
        :param vertices: Collection of vertices
        :type vertices: set
        :param edges: Collection of edges
        :type edges: set(set)
        :param adjacency_matrix: Adjacency matrix
        :type adjacency_matrix: list(list)
        """
        self._vertices = None
        self._edges = None
        self._adjacency_matrix = None
        self.vertices = vertices
        self.edges = edges
        self.adjacency_matrix = adjacency_matrix

    @property
    def vertices(self):
        """
        Vertices getter
        :return: vertices
        :rtype: set
        """
        return self._vertices

    @vertices.setter
    def vertices(self, vertices):
        """
        Vertices setter
        :param vertices:
        :type vertices: set
        """
        self._vertices = vertices

    @property
    def edges(self):
        """
        Edges getter
        :return: edges
        :rtype: set(tuple)
        """
        return self._edges

    @edges.setter
    def edges(self, edges):
        """
        Edges setter
        :param edges:
        :type edges: set(tuple)
        """
        self._edges = edges

    @property
    def adjacency_matrix(self):
        """
        Adjacency matrix getter
        :return: adjacency_matrix
        :rtype: list(list)
        """
        return self.adjacency_matrix

    @adjacency_matrix.setter
    def adjacency_matrix(self, matrix):
        """
        Adjacency matrix setter
        :param matrix:
        :type matrix: list(list)
        """
        self._adjacency_matrix = matrix
    
    def is_legal_graph(self, vertices, edges, adj):
        # Check edges
        assert(vert!=vert2 for edge in edges for vert, vert2 in edge), \
            "Not a graph; \nEdges cannot have both endpoints be the same vertex"
        # Check adjacency matrix
        assert(adj[[vert,vert]]==0 for vert in vertices), \
            "Not a graph; \nEdges cannot have both endpoints be the same vertex"
        assert(adj[entry] in [0,1] for entry in adj.keys()), \
            "Not a graph; \nVertices can only have at most 1 edge between them"
            
    def is_edge(self, v1, v2):
        """
        Returns true if v1,v2 is an edge
        """
        assert v1 in self.vertices, "v1 is not an edge."
        assert v2 in self.vertices, "v2 is not an edge."
        if v1 == v2:
            #Weighted graphs dont have self-adjacent vertices
            return False
        if self.edge_form(v1,v2) in self.edges():
            #Yes
            return True
        else:
            #Else statement for readability, fuck speed its 2016
            return False
        
    def is_an_edge(self, v1, *vertices):
        """Returns False if there is no edge from v1 to any of the edges in
        vertices, and returns the first edge encountered in any other case."""
        for vertex in vertices:
            if self.is_edge(v1, vertex):
                return self.edge_form(v1, vertex)
        return False
    
    def is_connected(self):
        """Returns True if graph is a connected graph, False else."""
        vertex = self.get_vertices().pop()
        distances = self.breadth_first(vertex)
        for v in distances.keys():
            if distances[v] == math.inf:
                #if there is a single unreachable vertex, then not connected
                return False
        #Every vertex is reachable, so, connected
        return True
    
    def add_vertex(self, vertex):
        """
        Adds a singular vertex to self.vertices and adds the vertex
        row and column to the adjacency matrix. 
        
        DOES NOT SET EDGES
        """
        vertices = self.get_vertices()
        #add it to vertices collection
        vertices.append(vertex)
        adj = self.get_adj()
        #add the vertex to the adjacency matrix
        for vert in vertices:
            adj[[vert, vertex]]=None
            adj[[vertex, vert]]=None
        self.set_vertices(vertices)
        self.set_adj(adj)
        
    
    def add_edge(self, edge):
        """
        Adds a singular edge to self.edges and self.adj
        Do not call this before the endpoints of the edge are known by
        the graph in self.vertices.
        """
        edges = self.get_edges()
        adj = self.get_adj()
        edges.append(edge)
        adj[edge[0], edge[1]] = 1
        adj[edge[1], edge[0]] = 1
        self.is_legal_graph(self.get_vertices(), edges, adj)
        self.set_edges(edges)
        self.set_adj(adj)
        self.is_legal_graph(self.get_vertices(), edges, adj)
        
    def add_edges(self, *edges):
        """Adds multiple edges with add_edge"""
        adj = self.adj
        for e in edges:
            assert (vertex in self.vertices for vertex in e), \
                "Edge has vertices that are not in the graph."
            self.add_edge(e)
            adj[e]=1
        self.set_adj(adj)
        
    def degree(self, vertex):
        """Returns the degree of the given vertex"""
        assert vertex in self.get_vertices(), "Vertex is not in the graph."
        degree = 0
        for other in self.get_vertices():
            if (vertex!=other) and (self.is_edge(vertex,other)):
                degree = degree + 1
        return degree
    
    def sum_of_degrees(self):
        """Returns the sum of degrees of the graph."""
        degree = 0
        for vertex in self.get_vertices():
            degree = degree + self.degree(vertex)
        return degree
    
    def adjacent(self, vertex):
        """Returns a set of vertices that are adjacent to v."""
        adjacents = {}
        for other in self.get_vertices():
            if self.is_edge(vertex,other):
                adjacents.append(other)
        return adjacents
        
    def other_vertices(self, *vertices):
        """Returns the collection of other vertices, distinct from vertex."""
        possible = self.get_vertices()
        for element in vertices:
            possible.remove(element)
        return possible
    
    def breadth_first(self, vertex):
        """returns a dictionary whose keys are the vertices, and whose values
        are the distances from vertex to each of these.
        
        output = {vertex: distance(input, vertex)}"""
        distances = {vert:math.inf for vert in self.get_vertices()}
        i = 0
        adjacents = [vertex]
        counted = []
        distances = {}
        while adjacents:
            for vertex in adjacents:
                distances[vertex] = i
                counted.append(vertex) 
            adjacents = [
                other 
                for other in self.other_vertices(*counted)
                if self.is_an_edge(other, adjacents)
             ]
        return distances
    
