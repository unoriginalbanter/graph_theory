try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from graph_theory import version


long_description = """
Python implemenation of graph theory objects, derived from a simple abstract base class, Graphlike. Each object is
defined with respect to its parent classes, designed for maximum mathematic accuracy. Behavior and methods are geared
towards a mathematic perspective.
"""


setup(
    name="graph_theory",
    version=version,
    description="Python Graph Theory Objects and Toolkit",
    long_description=long_description,
    author="Vincent Medina",
    author_email="vincent.medina@icloud.com",
    url="https://github.com/unoriginalbanter/graph_theory",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "opic :: Software Development :: Libraries :: Python Modules"
    ]
)