"""
Created on Apr 13, 2016

This is a base class to understand graphs in the computational sense.
It attempts to maintain the more abstract properties and "description" of
mathematical graphs as a collection of two objects (in this case, two
mutable collections), one of vertices, and edges. A third representation
implementing both is also used: adj -- the adjacency matrix, a dictionary
whose keys are the [vertex1,vertex2] ordered pair, and whose entries vary
depending on the implementation of Graphlike, but defaults to 0 when
no edge exists from vertex1 to vertex2.


This abstract class is designed to provide an abstract base class (ABC)
for the entirety of the graphlike objects included in this package:
graph, digraph, multigraph, psuedograph, psuedo

@author: unoriginalbanter
"""
import numbers
from typing import Union, Sequence, Set, AnyStr, SupportsComplex, Dict, Any, Iterable, Optional, overload


from abc import ABCMeta, abstractmethod, abstractproperty

from graph_theory.exceptions import VertexError, EdgeError, MatrixError


class Vertex(AnyStr):
    """
    This defines a vertex object. Generally speaking, this object shouldn't be anything cast in an extraordinary
    type or fashion, as these serve simply as labels for an abstract object.
    """
    def __init__(self, name: AnyStr, *args: Any, **kwargs: Any):
        """
        For the time being, a vertex is given almost exclusively by its name. Name should only have a type of str, int,
        or bytes (preferrably), or any object that is castable to str.

        Due to the risks involved in casting to string, please be wary of any potential name that would possibly be
        given to a vertex. It is recomended to only use strings, integers, or utf-8 bytes format, unless you are very
        comfortable with your data type.

        :param name: The identifier of the vertex.
        :type name: str or int or bytes
        """
        if type(name) == str:
            super(Vertex).__init__(name, *args, **kwargs)
        elif type(name) == bytes:
            super(Vertex).__init__(name, *args, **kwargs)
        elif type(name) == int:
            super(Vertex).__init__(name, *args, **kwargs)
        else:
            try:
                # Hashtag benefit of the doubt
                super(Vertex).__init__(name, *args, **kwargs)
            except TypeError:
                raise VertexError(
                    "TypeError",
                    "Name is not string-castable with the given args and kwargs, and of an invalid data type."
                )
            except:
                raise VertexError(
                    "CastingError",
                    "Unknown error during casting of vertex value."
                )
        self.name = name


class BaseEdge(Iterable[Vertex]):
    """
    Defines a base edge object. Due to the pluarlity of edge formats, we cannot define concretely how this object will
    behave just yet in here.
    """
    __metaclass__ = ABCMeta

    def __init__(self, vertex_pair: Sequence[Vertex], *args: Any, **kwargs: Any):
        """

        :param vertex_pair: The pair of vertices to convert to an edge
        :param args:  Other values
        :param kwargs: Other keyword values
        """
        super(BaseEdge, self).__init__(vertex_pair)
        self.vertices = vertex_pair


class BaseWeightedEdge(BaseEdge):
    """
    Defines a base weighted edge object. Extends BaseEdge by adding a value pair.
    """
    __metaclass__ = ABCMeta

    def __init__(self, vertex_pair: Sequence[Vertex], weight: SupportsComplex, *args: Any, **kwargs: Any):
        """
        :param vertex_pair:
        :param weight:
        :param args:
        :param kwargs:
        """
        if not isinstance(weight, numbers.Real):
            raise EdgeError(
                "TypeError",
                "All weighted edges must have a numeric.Real derived value. Got '{t}' instead.".format(
                    t=type(weight)
                )
            )
        super(BaseWeightedEdge).__init__(vertex_pair, *args, **kwargs)
        self.weight = weight

    def __repr__(self) -> str:
        """
        Define the represenation of WeightedDirectedEdge. This should be given to appear as if it were a dictionary,
        so that the weights are clearly identified with the vertex pairs.
        :return: repr
        :rtype: str
        """
        return "{v}, {w}".format(v=self.vertex_pair, w=self.weight)


Matrix = Dict[BaseEdge, numbers.Real]


class Graphlike(object):
    """
    abstract class, cannot instantiate it as a standalone instance
    """
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def __init__(self, vertices: Set[Vertex], edges: Set[BaseEdge], adjacency_matrix: Matrix):
        """
        Constructor
        """
        self._vertices = None
        self._edges = None
        self._adjacency_matrix = None
        self.vertices = vertices
        self.edges = edges
        self.adjacency_matrix = adjacency_matrix

    @classmethod
    @abstractmethod
    def is_legal(cls, vertices: Set[Vertex], edges: Set[BaseEdge], adjacency_matrix: Matrix) \
            -> None:
        """
        Provides the basest checks for is_legal:
            Are self.vertices and self.edges collected in a set data type?
            Is each vertex a Vertex type?
            Is each edge derived from BaseEdge type?
            Is each vertex and edge represented in the adjacency matrix?
        :param vertices:
        :type vertices: set(Vertex)
        :param edges:
        :type edges: set(BaseEdge)
        :param adjacency_matrix:
        :type adjacency_matrix: dict
        :raises VertexError: when Vertices don't match definition
        :raises EdgeError: when edges don't match definition
        :raises MatrixError: when adjacency matrix doesn't match definition
        """
        # Are the vertices in a set?
        if not isinstance(vertices, set):
            raise VertexError(
                "VertexCollectionTypeError",
                "Vertices are collected in a bad type. Expected: 'set', got: '{t}'".format(
                    t=type(vertices)
                )
            )
        # Are the edges in a set?
        if not isinstance(edges, set):
            raise EdgeError(
                "EdgeCollectionTypeError",
                "Edges are collected in a bad type. Expected: 'set', got: '{t}'".format(
                    t=type(edges)
                )
            )
        # Are the vertices each a 'Vertex'?
        if any(not isinstance(vertex, Vertex) for vertex in vertices):
            raise VertexError(
                "VertexTypeError",
                "Vertices should each be an instance of type 'Vertex'"
            )
        # Are the edges each an 'Edge'?
        if any(not isinstance(edge, BaseEdge) for edge in edges):
            raise EdgeError(
                "EdgeTypeError",
                "Each edge should be derived from 'BaseEdge'"
            )
        # Is each vertex represented in both axes of the adjacency matrix?
        for vertex in vertices:
            if not all(Graphlike.edge_form([vertex, other]) in adjacency_matrix.keys() for other in vertices):
                raise MatrixError(
                    "MissingVertexError",
                    "Missing vertex {v} from the adjacency_matrix.".format(
                        v=vertex
                    )
                )
        # Is each row and column value in the adjacency matrix a Vertex?
        for pair in adjacency_matrix.keys():
            if any(index not in vertices for index in pair):
                raise MatrixError(
                    "NonVertexIndex",
                    "Index {i} contains a non-vertex value.".format(
                        i=pair
                    )
                )
            if adjacency_matrix[pair] and pair not in edges:
                raise MatrixError(
                    "NonEdgeValue",
                    "Value at {i} has non-zero value despite no edge existing at this value.".format(
                        i=pair
                    )
                )
        # Is each edge represented in the adjacency matrix? Is each edge an Edge?
        for edge in edges:
            if not adjacency_matrix[edge]:
                raise MatrixError(
                    "EdgeNotRepresented",
                    "Edge {e} not represented in the adjacency matrix".format(
                        e=edge
                    )
                )
            if not isinstance(edge, BaseEdge):
                raise EdgeError(
                    "NotEdgeType",
                    "Edge {e} is not one of the edge types.".format(
                        e=edge
                    )
                )

    @property
    @abstractproperty
    def vertices(self) \
            -> Set[Vertex]:
        return self._vertices

    @vertices.setter
    @abstractproperty
    def vertices(self, vertices: Set[Vertex]) \
            -> None:
        self._vertices = vertices

    @property
    @abstractproperty
    def edges(self) \
            -> Set[BaseEdge]:
        return self._edges

    @edges.setter
    @abstractproperty
    def edges(self, edges: Set[BaseEdge]) \
            -> None:
        self._edges = edges

    @property
    @abstractproperty
    def adjacency_matrix(self) \
            -> Matrix:
        return self._adjacency_matrix

    @adjacency_matrix.setter
    @abstractproperty
    def adjacency_matrix(self, matrix: Matrix) \
            -> None:
        self._adjacency_matrix = matrix

    @abstractmethod
    def add_vertices(self, *vertices: Vertex) \
            -> None:
        """
        Adds a vertex to the graphlike object's vertices and adjacency_matrix
        properties.

        :param vertices: collection of vertices to add to Graphlike.vertices
        :type vertices: Vertex
        """
        return None

    @abstractmethod
    def add_edges(self, *edge: BaseEdge) \
            -> None:
        """
        Adds an edge to the graphlike object's edges and adjacency_matrix properties.
        """
        return None

    @abstractmethod
    def is_edge(self, potential_edge: BaseEdge, *args: Any, **kwargs: Any) \
            -> bool:
        """
        Returns true if potential_edge is an edge.
        :param potential_edge:
        :type potential_edge: BaseEdge
        :returns: is_edge
        :rtype: bool
        """
        return bool(potential_edge in self.edges)

    @abstractmethod
    def has_an_edge_with(self, v1: Vertex, *vertices: Vertex) -> Optional[Vertex]:
        """
        Returns the first edge encountered from v1 to any of the vertices,
        but if not, returns False.

        :param v1:
        :type v1: Vertex
        :param vertices:
        """
        return v1

    @abstractmethod
    def adjacent(self, vertex: Vertex) -> Set[Vertex]:
        """
        Returns a collection of vertices that are adjacent to vertex.
        :param vertex:
        :type vertex: Vertex
        :returns: adjacent
        :rtype: set(Vertex)
        """
        return self.vertices

    @classmethod
    @abstractmethod
    def other_vertices(cls, vertex: Vertex, *vertices: Vertex) -> Set[Vertex]:
        """
        Returns the collection of other vertices, distinct from vertex.
        :param vertex:
        :param vertices:
        :type vertex: Vertex
        :type vertices: Vertex
        :return other_vertices:
        :rtype: set(Vertex)
        """
        return set(vertices).difference(vertex)

    @classmethod
    @abstractmethod
    def edge_form(cls, vertex1: Vertex, vertex2: Vertex, *args: Any, **kwargs: Any) -> BaseEdge:
        """
        Returns the edge-format of v1, v2
        :param vertex1:
        :param vertex2:
        :param args:
        """
        return BaseEdge([vertex1, vertex2], *args, **kwargs)


class WeightedGraphlike(Graphlike):
    """
    Defines a weighted graphlike base object.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, vertices: Set[Vertex], edges: Set[BaseWeightedEdge], adjacency_matrix: Matrix):
        """
        Constructor.

        This class of object differs from Graphlike with only one minor difference: the edge objects are instead
        WeightedEdge objects.
        """
        super(WeightedGraphlike).__init__(vertices, edges, adjacency_matrix)
        self._vertices = None
        self._edges = None
        self._adjacency_matrix = None

    @classmethod
    @abstractmethod
    def is_legal(cls, vertices: Set[Vertex], edges: Set[BaseWeightedEdge], adjacency_matrix: Matrix) \
            -> None:
        """
        Provides the base checks for weighted graphlike object that aren't tested for in Graphlike.is_legal.
        Specifically, is each edge a weighted edge?
        :param vertices:
        :param edges:
        :param adjacency_matrix:
        :type vertices: set(Vertex)
        :type edges: set(BaseWeightedEdge)
        :type adjacency_matrix: dict
        """
        super(WeightedGraphlike).is_legal(vertices, edges, adjacency_matrix)
        if any(not isinstance(edge, BaseWeightedEdge) for edge in edges):
            raise EdgeError(
                "EdgeType",
                "Non weighted edge found in edges."
            )

    @property
    @abstractproperty
    def vertices(self) \
            -> Set[Vertex]:
        return self._vertices

    @vertices.setter
    @abstractproperty
    def vertices(self, vertices: Set[Vertex]) \
            -> None:
        self._vertices = vertices

    @property
    @abstractproperty
    def edges(self) \
            -> Set[BaseWeightedEdge]:
        return self._edges

    @edges.setter
    @abstractproperty
    def edges(self, edges: BaseWeightedEdge) \
            -> None:
        self._edges = edges

    @property
    @abstractproperty
    def adjacency_matrix(self) \
            -> Matrix:
        return self._adjacency_matrix

    @adjacency_matrix.setter
    @abstractproperty
    def adjacency_matrix(self, matrix: Matrix) \
            -> None:
        self._adjacency_matrix = matrix

    @abstractmethod
    def add_vertices(self, *vertex: Vertex) \
            -> None:
        """
        Adds a vertex to the graphlike object's vertices and adjacency_matrix
        properties.

        """
        return None

    @abstractmethod
    def add_edges(self, *edge: BaseWeightedEdge) \
            -> None:
        """
        Adds the edges to the graphlike object's edges and adjacency_matrix properties.
        """
        return None

    @overload
    def is_edge(self, potential_edge: BaseWeightedEdge, *args: Any, **kwargs: Any) \
            -> bool:
        """
        Is meant to be be ovverridden
        :param potential_edge:
        :type potential_edge: BaseWeightedEdge
        :param args:
        :param kwargs:
        :return:
        """
        return bool(potential_edge in self.edges)

    @abstractmethod
    def has_an_edge_with(self, v1: Vertex, *vertices: Vertex) \
            -> bool:
        """
        Returns the first edge encountered from v1 to any of the vertices,
        but if not, returns False.

        :param v1:
        :type v1: Vertex
        :param vertices:
        """
        return bool(vertices)

    @abstractmethod
    def adjacent(self, vertex: Vertex) -> Set[Vertex]:
        """
        Returns a collection of vertices that are adjacent to vertex.
        :param vertex:
        :type vertex: Vertex
        :returns: adjacent
        :rtype: set(Vertex)
        """
        return self.vertices

    @classmethod
    @abstractmethod
    def other_vertices(cls, vertex: Vertex, *vertices: Vertex) -> Set[Vertex]:
        """
        Returns the collection of other vertices, distinct from vertex.
        :param vertex:
        :param vertices:
        :type vertex: Vertex
        :type vertices: Vertex
        :return other_vertices:
        :rtype: set(Vertex)
        """
        return set(vertices).difference(vertex)

    @classmethod
    @abstractmethod
    def edge_form(cls, *params: Union[Iterable[Vertex], SupportsComplex], *args: Any, **kwargs: Any) -> BaseWeightedEdge:
        """
        Returns the edge-format of v1, v2
        :param vertex1:
        :param vertex2:
        :param args:
        """
        return BaseWeightedEdge(*params, *args, **kwargs)
