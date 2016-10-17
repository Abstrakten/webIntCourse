import numpy as np
from numpy.linalg import eig
import networkx as nx

# Intantiate graph
G = nx.Graph()

# Add nodes and edges to the graph
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_node(5)
G.add_node(6)
G.add_edge(1,2)
G.add_edge(2,3)
G.add_edge(1,3)
G.add_edge(3,4)
G.add_edge(4,5)
G.add_edge(4,6)
G.add_edge(5,6)

# Create the Laplacian matrix (L = D - A) from the graph as a dense matrix
L = nx.laplacian_matrix(G)
L_mat = L.todense()

# Compute the eigen decomposition of the Laplacian matrix
L_dec = eig(L_mat)

###
print(L_dec)
