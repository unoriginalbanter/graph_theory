'''
Created on Apr 13, 2016

@author: unoriginalbanter

Defines WeightedGraph class objects. 
Note: edges is a bit redundant. Equivalently, adj.keys()
'''
from . import weighted_digraph
class WeightedGraph(weighted_digraph.WeightedDigraph):
    '''
    Main properties:
        - vertices <set> The nodes of a graph
        - edges <list> The edges between vertices, a collection of ordered
                        pairs, does not track weights.
        - adj (Adjacency matrix), a dict whose keys are list-pairs of vertices
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
        assert(edge.keys()[0]!=edge.keys()[1] for edge in edges), \
            "Edges cannot have both endpoints be the same vertex"
        assert(adj[[vert,vert]]==0 for vert in vertices), \
            "Edges cannot have both endpoints be the same vertex"
        assert(adj[entry] in [0,1] for entry in adj.keys()), \
            "Vertices can only have at most 1 edge between them"
    
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
        
    
    def add_edge(self, edge, weight):
        '''
        Parameter:
         - edge is a <set(v1, v2)>
         - weight is your real number weight
        Adds a singular edge to self.edges and self.adj
        Do not call this before the endpoints of the edge are known by
        the graph in self.vertices.
        '''
        edges = self.get_edges()
        adj = self.get_adj()
        vertices = self.get_vertices()
        edges.append(edge)
        adj[edge[0], edge[1]] = weight
        adj[edge[1], edge[0]] = weight
        self.set_edges(edges)
        self.set_adj(adj)
        
        
    
    