'''
Created on Apr 13, 2016

@author: unoriginalbanter
'''
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
    
    def is_legal_digraph(self, vertices, edges, adj):
        assert(edge[0]!=edge[1] for edge in edges), \
            "Vertices cannot share and edge with themselves in a strict Digraph."
        assert(adj[[vert,vert]]==0 for vert in vertices), \
            "Vertices cannot share and edge with themselves in a strict Digraph."
        assert(all(vertices[i]!=vertices[i+1] for i in range(len(vertices)-1))), \
            "Only one vertex of a given name/index"
    
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
        
    
    def add_edges(self, **es):
        '''
        Adds a singular edge to self.edges and self.adj
        Do not call this before the endpoints of the edge are known by
        the graph in self.vertices.
        '''
        edges = self.get_edges()
        adj = self.get_adj()
        vs = es.keys()
        for v in vs:
            adj[v] = edges[v]
        self.is_legal_graph(self.get_vertices(), edges, adj)
        self.set_edges(edges)
        self.set_adj(adj)
        

        
    