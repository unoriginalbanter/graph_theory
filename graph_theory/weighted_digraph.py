'''
Created on Apr 13, 2016

@author: unoriginalbanter

A weighted digraph has directional edges; we track edges using ordered
list-pairs, and the adjacency matrix is thus non-symmetric across it's diagonal.
There is still no (v1, v1) edge for any vertex v1.
Also, edges are in the form of a dictionary, with the key being the classic
[v1, v2]. 
'''
from . import graphlike

class WeightedDigraph(graphlike.Graphlike):
    '''
    Main properties:
        vertices The nodes of a graph
        edges The edges between vertices, a set of tuple(v1,v2,w) entries,
                v1,v2 in edges. 
        adj (Adjacency matrix), a dict whose keys are list-pairs of vertices
                and whose values are 0 or 1;
                employs the dictionary representation of a matrix
    '''


    def __init__(self, verts=[], edges=set(), ad_m={}):
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
        assert(all(vertices[i]!=vertices[i+1] for i in range(len(vertices)-1))), \
            "Not a graph; \nOnly one vertex of a given name/index"
    
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
        
    
    def add_edges(self, **edges_weights):
        '''
        Adds a singular edge to self.edges and self.adj
        Do not call this before the endpoints of the edge are known by
        the graph in self.vertices.
        '''
        ew = edges_weights
        edges = self.get_edges()
        adj = self.get_adj()
        vs = ew.keys()
        for v in vs:
            adj[v] = edges[v]
        self.is_legal_graph(self.get_vertices(), edges, adj)
        self.set_edges(edges)
        self.set_adj(adj)
        
        
    
    