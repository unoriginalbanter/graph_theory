"""
Created on Apr 13, 2016

@author: unoriginalbanter
"""
from typing import Union, Tuple, Set, AnyStr, SupportsComplex, Dict, Any, Iterable, Optional, overload

import math

from graph_theory.objects.graphlike import Graphlike, Vertex, BaseEdge, Matrix
from graph_theory.exceptions import VertexError, EdgeError, MatrixError


class DirectedEdge(BaseEdge, tuple):
    """
    Defines a DirectedEdge object. Notably, the order that the vertices are named in the edge defines the edge as
    distinct. Ie., DirectedEdge(v1, v2) != DirectedEdge(v2, v1)
    """
    def __init__(self, vertex_pair: Tuple[Vertex], *args: Any, **kwargs: Any):
        """
        :param vertex_pair: The pair of vertices that form the directed edge
        :param args:
        :param kwargs:
        :type vertex_pair: list(Vertex)
        """
        if type(vertex_pair) != tuple:
            raise EdgeError(
                "TypeError",
                "Directed edge requires its vertex pair to come as a type 'tuple'. Got '{t}' instead.".format(
                    t=type(vertex_pair)
                )
            )
        super(DirectedEdge, self).__init__(vertex_pair, *args, **kwargs)


class Digraph(Graphlike):
    """
    :class_methods: is_legal_digraph
    :properties: vertices, edges, adjacency_matrix
    :methods: is_edge, has_an_edge_with
    """
    def __init__(self, vertices: Set[Vertex], edges: Set[DirectedEdge], adjacency_matrix=None):
        """
        :param vertices: the nodes of a digraph
        :param edges: the edges between vertices, a list of ordered pairs (list) of vertices
        :param adjacency_matrix: (optional) the adjacency matrix; a dict whose keys are 2-tuples of vertices and
            whose values are floats
        :type vertices: set
        :type edges: set
        :type adjacency_matrix: dict
        """
        super(Digraph, self).__init__(vertices, edges, adjacency_matrix)
        self._vertices = None
        self._edges = None
        self._adjacency_matrix = None
        self.vertices = set(vertices)
        self.edges = set(edges)
        self.adjacency_matrix = adjacency_matrix

    @property
    def vertices(self) \
            -> Set[Vertex]:
        """
        Vertices getter
        :return: vertices
        :rtype: set(Vertex)
        """
        return self._vertices

    @vertices.setter
    def vertices(self, vertices: Iterable[Vertex]) \
            -> None:
        """
        Vertices setter
        :param vertices:
        :type vertices: set
        """
        self._vertices = set(
            Vertex(v)
            for v in vertices
        )

    @property
    def edges(self) \
            -> Set[DirectedEdge]:
        """
        Edges getter
        :return: edges
        :rtype: set(DirectedEdge)
        """
        return self._edges

    @edges.setter
    def edges(self, edges: Iterable[Vertex]) \
            -> None:
        """
        Edges setter
        :param edges:
        :type edges: set(tuple)
        """
        self._edges = edges

    @property
    def adjacency_matrix(self) \
            -> Matrix:
        """
        Adjacency matrix getter
        :return: adjacency_matrix
        :rtype: list(list)
        """
        return self.adjacency_matrix

    @adjacency_matrix.setter
    def adjacency_matrix(self, matrix: Matrix) \
            -> None:
        """
        Adjacency matrix setter
        :param matrix:
        :type matrix: list(list)
        """
        self._adjacency_matrix = matrix

    @classmethod
    def is_legal(cls, vertices: Set[Vertex], edges: Set[DirectedEdge], matrix: Matrix) \
            -> None:
        """
        Does not overwrite Graphlike.is_legal()
        :param vertices:
        :param edges:
        :param matrix:
        :return:
        """
        super(Digraph).is_legal(vertices, edges, matrix)
        Digraph.is_legal_digraph(vertices, edges, matrix)

    @classmethod
    def is_legal_digraph(cls, vertices: Set[Vertex], edges: Set[DirectedEdge], matrix: Matrix) \
            -> None:
        """
        This method checks to see if the given combination of vertices, edges, and (adjacency) matrix is actually a
        legal digraph by the mathematic definition.

        A digraph is a graph whose edges are directional. That is (v1, v2) does not equal (v2, v1).

        :param vertices: vertices to check
        :param edges: edges to check
        :param matrix: adjacency matrix to check
        :return:
        """
        if any(not edge.isinstance(DirectedEdge) for edge in edges):
            raise EdgeError(
                "EdgeTypeError",
                "Found an edge not of type DirectedEdge"
            )
        if any(matrix[Digraph.edge_form(vert, other)] != 0
                for vert in vertices
                for other in vertices.difference(vert)
            ):
            raise EdgeError(
                "AutoAdjacent",
                "Vertices cannot share and edge with themselves in a strict Digraph."
            )

    def is_edge(self, edge: DirectedEdge, *args: Any, **kwargs: Any) \
            -> bool:
        """
        Returns true if v1,v2 is an edge. v1 and v2 MUST be contained in self.vertices. If not, raises VertexError.

        :param edge: The edge to check
        """
        if edge in self.edges:
            # We found the edge (v1, v2)
            return True
        else:
            # First validate that the vertices are indeed present in the vertices argument.
            v1, v2 = edge.vertices
            if v1 not in self.vertices:
                raise VertexError(
                    "ValueNotFound",
                    "Vertex {v} not found in the vertices of this graph: {vertices}".format(
                        v=v1,
                        vertices=self.vertices
                    )
                )
            if v2 not in self.vertices:
                raise VertexError(
                    "ValueNotFound",
                    "Vertex {v} not found in the vertices of this graph: {vertices}".format(
                        v=v2,
                        vertices=self.vertices
                    )
                )
            # We did not find the edge, and they are indeed vertices
            return False
    
    def has_an_edge_with(self, v1: Vertex, *vertices: Vertex) \
            -> Union[False, DirectedEdge]:
        """
        Returns False if there is no edge from v1 to any of the edges in
        vertices, and returns the first edge encountered in any other case.

        :param v1: The vertex to find edges to/from
        :param vertices: Collection of vertices to check if v1 has an edge to.
        """
        for vertex in vertices:
            if self.is_edge(v1, vertex):
                return self.edge_form(v1, vertex)
        return False
    
    @classmethod
    def edge_form(cls, v1: Vertex, v2: Vertex, *args, **kwargs):
        """Returns the edge-form of v1,v2, irregardless if v1,v2 is an edge.
        
        This is used for data-typing since the different graphlike objects use
        different data types for edges based on their mathematic properties.
        :param v1:
        :param v2:
        :type v1: Vertex
        :type v2: Vertex
        """
        return DirectedEdge(tuple([v1, v2]), *args, **kwargs)
    
    def add_vertices(self, *new_vertices):
        """
        Adds vertices to self.vertices and adds the vertex row and column to the adjacency matrix. If any new
        vertex would want edges between it and any other vertex in the digraph, this must be done in a separate
        method. (Specifically Digraph.add_edges())

        :param new_vertices: Vertex object to add.
        :type new_vertices: *Vertex
        """
        vertices = self.vertices.union(new_vertices)
        # Add the vertex to the vertex collection
        adj = self.adjacency_matrix
        # Add the vertex row and column to the adjacency matrix
        for vert in vertices:
            for vertex in new_vertices:
                # Assign the value to zero (Assumes no new edges)
                adj[Digraph.edge_form(vert, vertex)] = 0
                adj[Digraph.edge_form(vertex, vert)] = 0
        self.vertices = vertices
        self.adjacency_matrix = adj
        
    def add_edges(self, *es):
        """
        Adds multiple edges to self.edges and self.adj. Do not call this before the endpoints of the edge are known by
        the graph in self.vertices.
        :param es:
        :type es: *DirectedEdge
        """
        edges = self.edges()
        adj = self.adjacency_matrix()
        for edge in es:
            adj[edge] = 1
        edges = edges.union(es)
        self.is_legal_digraph(self.vertices, edges, adj)
        self.edges = edges
        self.adjacency_matrix = adj
        
    def in_degree(self, vertex):
        """
        Returns the indegree of the given vertex.
        :param vertex:
        :type vertex: Vertex
        """
        degree = 0
        # This is faster for large matrices with many edges, relatively slow but otherwise, computers are fast so NBD
        for other_vert in self.vertices.difference(vertex):
            if self.edge_form(other_vert, vertex) in self.edges:
                degree += 1
        return degree
    
    def out_degree(self, vertex):
        """
        Returns the outdegree of a given vertex.
        :param vertex:
        :type vertex: Vertex
        """
        degree = 0
        # This is faster for large matrices with many edges, relatively slow otherwise
        # but otherwise, computers are fast so NBD
        for other_vert in self.vertices:
            if self.edge_form(vertex, other_vert) in self.edges:
                degree += 1
        return degree
    
    def sum_of_degrees(self):
        """Returns the sum of degrees of the graph. Recall that:
            (SUM(in_degree(v)) FORALL v IN vertices) is equal to
            (SUM(out_degree(v)) FORALL v IN vertices)
            
        Since they are equal, it does not matter which degree we are summing,
        but for sake of documentation, it is the in_degree
        :return sum_of_degrees:
        :rtype: int
        """
        sum_of_degrees = 0
        for vertex in self.vertices:
            sum_of_degrees += self.in_degree(vertex)
        return sum_of_degrees
    
    def adjacent(self, vertex):
        """
        Returns a set of vertices that are adjacent to v.

        :param vertex:
        :type vertex: Vertex
        :return: adjacents
        :rtype: set(Vertex)
        """
        adjacents = set()
        for other in self.vertices():
            if self.is_edge(vertex, other):
                adjacents.union(other)
        return adjacents
    
    def other_vertices(self, *vertices):
        """
        Returns the collection of other vertices, distinct from the args vertices.
        :arg vertices:
        :type vertices: Vertex
        """
        possible = self.vertices
        for element in vertices:
            possible = possible.differnce(element)
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

        :param vertex: A vertex
        :type vertex: Vertex
        :return distances:
        :rtype: dict(dict)
        """
        assert vertex in self.vertices, "Given vertex is not a member of the digraph."
        adj = self.adjacency_matrix
        labels = {
            vert: math.inf
            for vert in self.vertices
        }
        path = {
            vert: []
            for vert in self.vertices
        }
        collection = self.vertices.remove(vertex)
        labels[vertex] = 0
        while collection:
            # While there are values to check for
            for vert in collection:
                # Select a lowest-labeled vertex
                if (labels[vert] <= labels[other] for other in collection):
                    vertex = vert
                    break
            # Stop counting vertex
            collection.difference(vertex)
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
        distances = {}
        for vertex in self.vertices:
            distances[vertex] = {
                'path': path[vertex],
                'distance': labels[vertex]
            }
