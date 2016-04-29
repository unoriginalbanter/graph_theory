'''
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
'''
from . import digraph

class Graph(digraph.Digraph):
    '''
    Main properties:
        vertices The nodes of a graph
        edges The edges between vertices, a collection of pairs (in this case,
                a set of two vertices)
        adj (Adjacency matrix), a dict whose keys are list-pairs of vertices
                and whose values are 0 or 1;
                employs the dictionary representation of a matrix
    '''


    def __init__(self, verts=[], edges=[], ad_m={}):
        '''
        Constructor
        '''
        self.vertices=verts
        self.edges=edges
        self.adj=ad_m
        
            
    def get_vertices(self):
        return self.vertices
    
    def set_vertices(self, vertices):
        self.vertices=vertices
        
    property(get_vertices, set_vertices)
    
    def get_edges(self):
        return self.edges
    
    def set_edges(self, edges):
        self.edges=edges
        
    property(get_edges, set_edges)
    
    def set_adj(self, adj):
        self.adj = adj
        
    def get_adj(self):
        return self.adj
    
    def is_legal_graph(self, vertices, edges, adj):
        assert(edge[0]!=edge[1] for edge in edges), \
            "Not a graph; \nEdges cannot have both endpoints be the same vertex"
        assert(adj[[vert,vert]]==0 for vert in vertices), \
            "Not a graph; \nEdges cannot have both endpoints be the same vertex"
        assert(adj[entry] in [0,1] for entry in adj.keys()), \
            "Not a graph; \nVertices can only have at most 1 edge between them"
    
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
        
    
    def add_edge(self, edge):
        '''
        Adds a singular edge to self.edges and self.adj
        Do not call this before the endpoints of the edge are known by
        the graph in self.vertices.
        '''
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
        '''Adds multiple edges with add_edge'''
        for e in edges:
            self.add_edge(e)
        
    