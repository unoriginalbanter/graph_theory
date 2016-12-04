"""
Created on Apr 13, 2016

@author: unoriginalbanter

Defines WeightedGraph class objects. 
Note: edges is a bit redundant. Equivalently, adj.keys()
"""
from graph_theory.objects import weighted_digraph
class WeightedGraph(weighted_digraph.WeightedDigraph):
    """
    Main properties:
        - vertices <set> The nodes of a graph
        - edges <dict> The edges between vertices, a dict of unordered
                        pairs, tracks weights as the value.
        - adj (Adjacency matrix), a dict whose keys are list-pairs of vertices
                and whose values are float-type weights, or None if no edge is
                present;
                employs the dictionary representation of a matrix
    """
    def __init__(self, vertices, edges, ad_m):
        """
        Constructor

        :param vertices:
        :param edges:
        :param adjacency_matrix:

        """
        self._vertices = self.set_vertices(vertices)
        self._edges = self.set_edges(edges)
        self._adj = ad_m

    @property
    def vertices(self):
        return self._vertices

    def vertices(self):
        return self._vertices
    
    def set_vertices(self, vertices):
        self.vertices = set(vertices)
        
    property(get_vertices, set_vertices)
    
    def get_edges(self):
        return self.edges
    
    def set_edges(self, edges):
        self.edges = set(edges)
        
    property(get_edges, set_edges)
    
    def set_adj(self, adj):
        self.adj = adj
        
    def get_adj(self):
        return self.adj
    
    def edge_form(self, v1, v2, value=1.0):
        """Returns the edge-form of v1,v2, irregardless if v1,v2 is an edge.
        
        Since weighted graphs require a weight, edge_form takes a value; if no
        value is present, value defaults to 1.
        
        This is used for data-typing since the different graphlike objects use
        different data types for edges based on their mathematic properties.
        """
        return {{v1,v2}:value}
    
    def is_legal_graph(self, vertices, edges, adj):
        assert(list(edge.keys())[0]!=list(edge.keys())[1] for edge in edges), \
            "Edges cannot have both endpoints be the same vertex"
        assert(adj[set([vert,vert])]==0 for vert in vertices), \
            "Edges cannot have both endpoints be the same vertex"
        assert(adj[entry] in [0,1] for entry in adj.keys()), \
            "Vertices can only have at most 1 edge between them"
            
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
    
    def add_vertex(self, vertex):
        """
        Adds a singular vertex to self.vertices and adds the vertex
        row and column to the adjacency matrix
        """
        vertices = self.get_vertices()
        vertices.append(vertex)
        adj = self.get_adj()
        for vert in vertices:
            adj[[vert, vertex]]=None
            adj[[vertex, vert]]=None
        vertices.append(vertex)
        self.set_vertices(vertices)
        self.set_adj(adj)
        
    
    def add_edge(self, edge, weight):
        """
        Parameter:
         - edge is a <set(v1, v2)>
         - weight is your real number weight
        Adds a singular edge to self.edges and self.adj
        Do not call this before the endpoints of the edge are known by
        the graph in self.vertices.
        """
        edges = self.get_edges()
        adj = self.get_adj()
        #Add the edge to self.edges
        edges[edge] = weight
        v1 = edge.pop()
        v2 = edge.pop()
        adj[v1,v2] = weight
        adj[v2,v1] = weight
        self.set_edges(edges)
        self.set_adj(adj)
        
    def degree(self, vertex):
        """Returns the degree of the given vertex"""
        assert vertex in self.get_vertices(), "Vertex is not in the graph."
        degree = 0
        for other in self.get_vertices():
            if self.is_edge(vertex,other):
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
    

    