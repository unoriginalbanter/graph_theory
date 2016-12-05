"""
Definitions of package-specific errors and exceptions.

Author: Vincent Medina
2016-12-04
"""
from abc import ABCMeta


class GraphTheoryException(Exception):
    """
    Base exception class for graph_theory package.
    """
    __metaclass__ = ABCMeta

    def __init__(self, expression, message):
        """
        Constructor
        :param expression: Error
        :param message: Error message
        """
        self.expression = expression
        self.message = message


class VertexError(GraphTheoryException):
    """
    Raised when a bad collection of objects is attempting to be set as a Graphlike object's vertices property.
    """
    def __init__(self, expression, message, vertices=None, edges=None):
        """
        :param expression:
        :param message:
        :param vertices: collection of vertices (optional)
        :param edges: collection of edges (optional)
        """
        self.expression = expression
        self.message = message
        self.vertices = vertices
        self.edges = edges


class EdgeError(GraphTheoryException):
    """
    Raised when a bad collection of objects is attempting to be set as a Graphlike object's edges property.
    """
    def __init__(self, expression, message, vertices=None, edges=None):
        """
        :param expression:
        :param message:
        :param vertices: collection of vertices (optional)
        :param edges: collection of edges (optional)
        """
        self.expression = expression
        self.message = message
        self.vertices = vertices
        self.edges = edges


class MatrixError(GraphTheoryException):
    """
    Raised when a bad collection of objects is attempting to be set as a Graphlike object's vertices property.
    """
    def __init__(self, expression, message, matrix=None):
        """
        :param expression:
        :param message:
        :param matrix:
        """
        self.expression = expression
        self.message = message
        self.matrix = matrix