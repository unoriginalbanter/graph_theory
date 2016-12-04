"""
Created on Apr 19, 2016

@author: unoriginalbanter

This module contains methods that operate on various graphlike objects to find
values related to mathematic connectivity within graphs, including distance
searches, paths, cycles, minimum weight trees, etc. For proper implementation,
see each method.
"""

from graph_theory.objects import graph


def complete_graph(n):
    """
    Creates and returns a complete graph of order n, K_n.
    The vertices created are named with integers from 0 to n for ease
    of navigation. Though, this distinction is arbitrary in complete graphs.

    :param n: order of desired complete graph
    :type n: int
    :returns: complete_graph
    """
    complete_graph = graph.Graph()
    for i in range(n):
        complete_graph.add_vertex(i)
        complete_graph.add_edges(
            {v, i} for v in complete_graph.get_vertices()
            if v != i
        )
    return complete_graph


def is_complete_graph(graph):
    """
    Returns true if given graph is a complete graph, false else.
    Checks adjacency matrix for nonzero entries, so, returns true if the edges 
    exist even in directed and weighted graphs.

    :param graph: Graph object to de determined if it is a complete graph.
    :type graph: graph.Graph
    :returns: is_complete_graph
    :rtype: bool
    """
    adjacency = graph.get_adj()
    for key in adjacency.keys():
        if adjacency[key] == None:
            return False
    return True


def is_graphical_sequence(sequence):
    """
    Returns true if parameter sequence is a graphical sequence (a sequence that
    can describe the degree of the vertices of a graph).

    :param sequence: Sequence of integers to be determined if it is a graphical sequence (degree sequence of a graph)
    :type sequence: list(int)
    :returns: is_graphcal_sequence
    :rtype: bool
    """
    seq = [integer for integer in sequence.sort(reverse=True)]
    p = len(seq)
    for d in seq:
        if d >= p-1:
            # if there is an integer d that is d>=(p=1), is not graphical
            return False
        elif d < 0:
            # if there is a negative integer in sequence, then it is not graphical
            return False
    if (d == 0 for d in seq):
        # if all terms are zero, then the sequence is graphical
        return True
    # ELSE: remove the first (largest) term d1, and subtract 1 from next d1 terms
    first_term = seq.pop(0)
    for i in range(first_term):
        seq[i] -= 1
    # ELSE (cont): repeat
    is_graphical_sequence(seq)

