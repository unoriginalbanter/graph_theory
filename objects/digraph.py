'''
Created on Apr 13, 2016

@author: unoriginalbanter
'''
import math

from . import graphlike

class Digraph(graphlike.Graphlike):
    '''
    Main properties:
        vertices The nodes of a digraph
        edges The edges between vertices, a list of ordered pairs <list>
        adj (Adjacency matrix), a dict whose keys are list-pairs of vertices
                and whose values are floats;
                employs the dictionary representation of a matrix
    '''


    def __init__(self, verts=[], edges={}, ad_m={}):
        '''
        @param(verts) the nodes of a digraph,
        @param(edges) the edges between vertices, a list of ordered pairs (list)
            of vertices
        @param(adj) the adjacency matrix; a dict whose keys are list-pairs of 
            vertices and whose values are floats
        '''
        self.vertices=self.add_vertices(verts)
        self.edges=self.add_edges(edges)
        self.adj=ad_m
        
            
    def get_vertices(self):
        """vertices getter"""
        return self.vertices
    
    def set_vertices(self, vertices):
        """vertices setter"""
        self.vertices=vertices
        
    property(get_vertices, set_vertices)
    
    def get_edges(self):
        """edges getter"""
        return self.edges
    
    def set_edges(self, edges):
        """edges setter"""
        self.edges=edges
        
    property(get_edges, set_edges)
    
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
        '''
        Adds a singular vertex to self.vertices and adds the vertex
        row and column to the adjacency matrix
        '''
        vertices = self.get_vertices()
        vertices.append(vertex)
        adj = self.get_adj()
        for vert in vertices:
            adj[[vert, vertex]]=0
            adj[[vertex, vert]]=0
        vertices.append(vertex)
        self.set_vertices(vertices)
        self.set_adj(adj)
        
    def add_edges(self, *es):
        '''
        Adds a singular edge to self.edges and self.adj
        Do not call this before the endpoints of the edge are known by
        the graph in self.vertices.
        '''
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