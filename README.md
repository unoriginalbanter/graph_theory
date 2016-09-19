# graph_theory
Author: unoriginalbanter (V. Medina)
Version 0.0.2-1a

## Synopsis
__NOTE: IF YOU WERE LOOKING FOR BAR GRAPHS OR LINE GRAPHS, THIS IS NOT THE
PACKAGE FOR YOU.__


graph_theory is a Python package developed in Python3.5 (2.7 untested). 
Objects in the inheritance tree of *graphlike*, are an object-oriented
understanding of the mathematics of graph theory, an extensive and vibrantly
rich field of study, whose principals and results are so well-generalized that
their applications cover such diverse fields as network security, electrical
engineering, linguistics, chemistry, physics... For more information, consult
your local wikipedia:
[Wikipedia page on graph theory](https://en.wikipedia.org/wiki/Graph_theory)

(Note: the author implemented algorithms as collected and described by
Ronald Gould in [*Graph Theory*](http://www.amazon.com/Graph-Theory-Dover-Books-Mathematics/dp/0486498069))


## Objective (A Note From the Author)
This package serves as an exploration of the author's understanding of Python's
interactions between Abstract Base Classes and the more "Pythonic" style of 
duck-typing code (if it quacks like a duck, assume it has callable duck 
methods.) By structuring graphlike objects via ABCs, we can reference 
isinstance() methods in subsequent "operations" modules for try/raise exception 
handling in object-type algorithms (say, for Kruskal's Algorithm for Minimum 
Weight-Spanning Trees from weighted connected graphs), while allowing for a 
clear structure of properties of each of the various kinds of graphlike objects 
of interest. 

Also, for those programmers who wish to implement graph theory solutions to
certain applicable technical issues, and yet who do not have a background in
mathematics, this structure allows for better intuitive understanding of the
object inheritance Trees, pun intended.

See: [PEP 3119 -- Introducing Abscract Base Classes](https://www.python.org/dev/peps/pep3119/)


## Usage
Since the project is in development, usage is still very limited. However,
creation of Graphs, Digraphs, and their weighted counterparts are still
callable and creatable. For example, importing graph.py, we can create the
complete graph of order 3 by hard-code,

>import graphlike_connectivity as graphlike
>k3 = graphlike.complete_graph(3)