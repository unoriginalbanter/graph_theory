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


class InvalidVertices(GraphTheoryException):
    """
    Raised when a bad collection of objects is attempting to be set as a Graphlike object's vertices property.
    """
    def __init__(self, expression, message):
        """
        :param expression:
        :param message:
        """
        self.expression = expression
        self.message = message