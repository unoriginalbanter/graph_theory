"""
Created on Apr 13, 2016

@author: unoriginalbanter

A weighted digraph has directional edges; we track edges using ordered
list-pairs, and the adjacency matrix is thus non-symmetric across it's diagonal.
There is still no (v1, v1) edge for any vertex v1.
Also, edges are in the form of a dictionary, with the key being the classic
[v1, v2]. 
"""
import math


from graph_theory.exceptions import *
from graph_theory.objects import digraph
from graph_theory.objects.graphlike import BaseWeightedEdge


class WeightedDirectedEdge(BaseWeightedEdge, digraph.DirectedEdge):
    """
    :class: WeightedDirectedEdge
        Defines a Weighted Directed Edge.
        Since WeightedDirectedEdge objects inherit from both DirectedEdge and BaseWeightedEdge, we can immediately see
        that the object has two important properties, vertex_pair and weight. The vertex_pair is an ordered 2-tuple

       :attribute: vertex_pair
       :attribute: weight
    """
    def __init__(self, vertex_pair, weight, *args, **kwargs):
        """
        :param vertex_pair:
        :type vertex_pair: tuple
        :param weight:
        :type weight: numbers.Real
        :param args:
        :param kwargs:
        """
        super(WeightedDirectedEdge).__init__(vertex_pair, weight, *args, **kwargs)


class WeightedDigraph(digraph.Digraph):
    """
    Main properties:
        vertices The nodes of a graph
        edges The edges between vertices, a set of tuple(v1,v2,w) entries, v1,v2 in vertices. These are purposefully
            kept as a set rather than a list.
        adj (Adjacency matrix), a dict whose keys are list-pairs of vertices and whose values are 0 or 1; employs the
            dictionary representation of a matrix
    """
    def __init__(self, vertices=None, edges=None, adjacency_matrix=None):
        """
        Constructor

        :param vertices: Set of vertices
        :param edges: Set of tuple entries (vertex1, vertex2, weight)
        :param adjacency_matrix:
        :type vertices: set(Vertex)
        :type edges: set(Weighted
        """
        super(WeightedDigraph).__init__(vertices, edges, adjacency_matrix)
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
        :type vertices: set(Vertex)
        """
        self._vertices = vertices

    @property
    def edges(self):
        """
        Edges getter
        :return: edges
        :rtype: set(WeightedDirectedEdge)
        """
        return self._edges

    @edges.setter
    def edges(self, edges):
        """
        Edges setter
        :param edges:
        :type edges: set(WeightedDirectedEdge)
        """
        self._edges = edges

    @property
    def adjacency_matrix(self):
        """
        Adjacency matrix getter
        :return: adjacency_matrix
        :rtype: dict({WeightedDirectedEdge: numbers.Real})
        """
        return self.adjacency_matrix

    @adjacency_matrix.setter
    def adjacency_matrix(self, matrix):
        """
        Adjacency matrix setter
        :param matrix:
        :type matrix: dict({WeightedDirectedEdge: numbers.Real})
        """
        self._adjacency_matrix = matrix
    
    def is_legal(self, vertices, edges, adjacency_matrix):
        """
        Is a simple call to Graphlike.is_legal()
        :param vertices:
        :type vertices: set(Vertex)
        :param edges:
        :type edges: set(WeightedEdges)
        :param adjacency_matrix:
        :return:
        """
        super(WeightedDigraph).is_legal(vertices, edges, adjacency_matrix)
        WeightedDigraph.is_legal_weighted_digraph(vertices, edges, adjacency_matrix)

    @classmethod
    def is_legal_weighted_digraph(cls, vertices, edges, matrix):
        """
        Checks that the given combination of vertices edges and (adjacency) matrix together meet the requirements
        of being a legal weighted digraph. Does not currently have a check in place for vertices
        :param vertices:
        :param edges:
        :param matrix:
        :type vertices: set(Vertex)
        :type edges: set(WeightedDirectedEdge)
        :type matrix: dict({WeightedDirectedEdge: numbers.Real})
        :return:
        """
        if all(edge.isinstance(WeightedDirectedEdge) for edge in edges):
            pass
        else:
            raise EdgeError(
                "TypeError",
                "All edges in a weighted digraph must be both weighted and directional. Edges: {e}"
            )
        if any(matrix[key] != key.weight for key in matrix):
            raise MatrixError(
                "TypeError",
                "All edge values must correspond to their weights."
            )

    @classmethod
    def edge_form(cls, vertex1, vertex2, *args, **kwargs):
        """
        Returns the edge-form of v1,v2, irregardless if v1,v2 is an edge.

        The first parameter in args should be weight.
        
        This is used for data-typing since the different graphlike objects use
        different data types for edges based on their mathematic properties.
        :param vertex1:
        :type vertex1: Vertex
        :param vertex2:
        :type vertex2: Vertex
        :arg weight:
        :type weight: numbers.Real
        :return: edge_form
        :rtype: WeightedDirectedEdge
        """
        return WeightedDirectedEdge(tuple([vertex1, vertex2]), *args, **kwargs)
    
    def is_edge(self, v1, v2, *args, **kwargs):
        """
        Returns true if there exists some edge between v1 and v2. Can also return true if the optional argument
        weight is provided.

        :param v1:
        :type v1: Vertex
        :param v2:
        :type v2: Vertex
        :arg weight: (Optional) Returns True if there is an edge from v1 to v2 AND that edge has weight given.
        """
        if args:
            # Checking everything
            weight = args[0]
            if self.edge_form(v1, v2, weight) in self.edges:
                return True
            else:
                return False
        else:
            # Iterate through each edge to see if they share the same vertex_pair.
            # Fake weight it dont matter
            weight = [1]
            if any(edge.vertex_pair == self.edge_form(v1, v2, weight).vertex_pair for edge in self.edges):
                return True
            else:
                return False
    
    def has_an_edge_with(self, v1, *vertices):
        """
        Returns False if there is no edge from v1 to any of the edges in vertices, and returns the first edge
        encountered in any other case.
        :param v1:
        :type v1: Vertex
        :argument vertices:
        :type vertices: *Vertex
        """
        for vertex in vertices:
            if self.is_edge(v1, vertex):
                return self.edge_form(v1, vertex)
        return False
    
    def add_vertex(self, vertex):
        """
        Adds a singular vertex to self.vertices and adds the vertex
        row and column to the adjacency matrix
        """
        vertices = self.get_vertices()
        vertices.append(vertex)
        adj = self.get_adj()
        for vert in vertices:
            adj[[vert, vertex]]=0
            adj[[vertex, vert]]=0
        vertices.append(vertex)
        self.set_vertices(vertices)
        self.set_adj(adj)
        
    def add_edges(self, **edges_weights):
        """
        Adds a singular edge to self.edges and self.adjacency_matrix
        Do not call this before the endpoints of the edge are known by
        the graph in self.vertices.
        """
        ew = edges_weights
        edges = self.get_edges()
        adj = self.get_adj()
        vs = ew.keys()
        for v in vs:
            adj[v] = edges[v]
        self.is_legal_graph(self.get_vertices(), edges, adj)
        self.set_edges(edges)
        self.set_adj(adj)
        
    def in_degree(self, vertex):
        """Returns the indegree of the given vertext."""
        assert vertex in self.get_vertices(), "Vertex must be in the graph."
        degree = 0
        #This is faster for large matrices with many edges, relatively slow otherwise
        #but otherwise, computers are fast so NBD
        for other_vert in self.get_vertices():
            if [other_vert, vertex] in self.get_edges():
                degree = degree + 1
        return degree
    
    def out_degree(self, vertex):
        """Returns the outdegree of a given vertex"""
        degree = 0
        #This is faster for large matrices with many edges, relatively slow otherwise
        #but otherwise, computers are fast so NBD
        for other_vert in self.get_vertices():
            if [vertex, other_vert] in self.get_edges():
                degree = degree + 1
        return degree
    
    def sum_of_degrees(self):
        """Returns the sum of degrees of the graph. Recall that:
            (SUM(in_degree(v)) FORALL v IN vertices) is equal to
            (SUM(out_degree(v)) FORALL v IN vertices)
            
        Since they are equal, it does not matter which degree we are summing,
        but for sake of documentation, it is the in_degree
        """
        sum = 0
        for vertex in self.get_vertices():
            sum = sum + self.in_degree(vertex)
        return vertex
    
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
        
    def dijkstra_distance(self, vertex):
        """Performs Dijkstra's Distance Algorithm. Returns the distance from
        vertex to each of the other vertices.
        
        Output format: 
            output = {
                vertex: {
                    'path':[v1,v2,...], 
                    distance:dist(input, vertex)
                }
            }
        """
        assert vertex in self.vertices, "Given vertex is not a member of the digraph."
        adj = self.get_adj()
        #Track the distance here
        labels = {
            vert:math.inf 
            for vert in self.get_vertices()
        }
        #Track a shortest path (NOTE: shortest path may not be unique)
        path = {
            vert:[]
            for vert in self.get_vertices()
        }
        #Track the collection of vertices that hasn't been counted yet
        collection = self.get_vertices().remove(vertex)
        labels[vertex] = 0
        while collection:
            #While there are values to check for
            for vert in collection:
                #Select a lowest-labeled vertex
                if (labels[vert] <= labels[other] for other in collection):
                    vertex = vert
                    break
            #Stop counting vertex
            collection.remove(vertex)
            edges = [
                edge
                for edge in self.edges
                if edge[0] == vertex
            ]
            for edge in edges:
                w = edge[1]
                if (w in collection) and (labels[w] > labels[vertex] + adj[edge]):
                    labels[w] = labels[vertex] + adj[edge]
                    path[w].append(vertex)
        return {
            vertex: {
                'path':path[vertex],
                'distance':labels[vertex]
            }
        }