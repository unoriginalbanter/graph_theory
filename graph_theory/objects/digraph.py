"""
Created on Apr 13, 2016

@author: unoriginalbanter
"""
import math

from graph_theory.objects.graphlike import Graphlike


class Digraph(Graphlike):
    """
    Main properties:
        vertices The nodes of a digraph
        edges The edges between vertices, a list of ordered pairs <list>
        adj (Adjacency matrix), a dict whose keys are list-pairs of vertices
                and whose values are floats;
                employs the dictionary representation of a matrix
    """
    def __init__(self, vertices=None, edges=None, adjacency_matrix=None):
        """
        :param vertices: the nodes of a digraph
        :param edges: the edges between vertices, a list of ordered pairs (list) of vertices
        :param adjacency_matrix: (optional) the adjacency matrix; a dict whose keys are 2-tuples of vertices and
            whose values are floats
        :type vertices: list
        :type edges: list
        :type adjacency_matrix: dict
        """

        self._vertices = self.add_vertices(vertices)
        self._edges = self.add_edges(edges)
        self._adj = adjacency_matrix

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
    
    def get_edges(self):
        """edges getter"""
        return self.edges
    
    def set_edges(self, edges):
        """
        Wrapper for edges setter
        """
        self.edges = edges

    def set_adj(self, adj):
        """adj setter"""
        self.adj = adj
        
    def get_adj(self):
        """adj getter"""
        return self.adj
    
    def is_legal_digraph(self, vertices, edges, adj):
        assert(edge[0]!=edge[1] for edge in edges), \
            "Vertices cannot share and edge with themselves in a strict Digraph."
        assert(adj[[vert,vert]]==0 for vert in vertices), \
            "Vertices cannot share and edge with themselves in a strict Digraph."
        assert(all(vertices[i]!=vertices[i+1] for i in range(len(vertices)-1))), \
            "Only one vertex of a given name/index"
            
    def is_edge(self, v1, v2):
        """Returns true if v1,v2 is an edge"""
        assert v1 in self.vertices, "v1 is not an edge."
        assert v2 in self.vertices, "v2 is not an edge."
        if self.edge_form(v1, v2) in self.edges:
            return True
        return False
    
    def is_an_edge(self, v1, *vertices):
        """Returns False if there is no edge from v1 to any of the edges in
        vertices, and returns the first edge encountered in any other case."""
        for vertex in vertices:
            if self.is_edge(v1, vertex):
                return self.edge_form(v1, vertex)
        return False
    
    def edge_form(self, v1, v2, value):
        """Returns the edge-form of v1,v2, irregardless if v1,v2 is an edge.
        
        This is used for data-typing since the different graphlike objects use
        different data types for edges based on their mathematic properties.
        """
        return [v1,v2]
    
    def add_vertex(self, vertex):
        """
        Adds a singular vertex to self.vertices and adds the vertex
        row and column to the adjacency matrix
        """
        vertices = self.get_vertices()
        vertices.append(vertex)
        #Add the vertex to the vertex collection
        adj = self.get_adj()
        #Add the vertex row and column to the adjacency matrix
        for vert in vertices:
            adj[[vert, vertex]]=0
            adj[[vertex, vert]]=0
        self.set_vertices(vertices)
        self.set_adj(adj)
        
    def add_edges(self, *es):
        """
        Adds a singular edge to self.edges and self.adj
        Do not call this before the endpoints of the edge are known by
        the graph in self.vertices.
        """
        edges = self.get_edges()
        adj = self.get_adj()
        for ed in es:
            adj[ed] = 1 
        edges.extend(es)
        self.is_legal_graph(self.get_vertices(), edges, adj)
        self.set_edges(edges)
        self.set_adj(adj)
        
    def in_degree(self, vertex):
        """
        Returns the indegree of the given vertext."""
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
        sum_of_degrees = 0
        for vertex in self.get_vertices():
            sum_of_degrees += self.in_degree(vertex)
        return sum_of_degrees
    
    def adjacent(self, vertex):
        """Returns a set of vertices that are adjacent to v."""
        adjacents = {}
        for other in self.get_vertices():
            if self.is_edge(vertex,other):
                adjacents.append(other)
        return adjacents
    
    def other_vertices(self, *vertices):
        """Returns the collection of other vertices, distinct from the args vertices."""
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
        labels = {
            vert:math.inf 
            for vert in self.get_vertices()
        }
        path = {
            vert:[]
            for vert in self.get_vertices()
        }
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