import numpy as np
import networkx
import matplotlib.pyplot as pyplot
import sys
import graph
import coloring


def create_graph(incidence_matrix):
    G = networkx.Graph()
    for vertice in range(graph.order(incidence_matrix)):
        for neighbour in graph.adjacent_vertices(incidence_matrix, vertice):
            if not G.has_edge(neighbour, vertice):
                G.add_edge(vertice, neighbour)
    return G


if __name__ == '__main__':
    # Analisa as matrizes com a função `np.mat` e passa elas para
    # `np.array`s.
    lines = []
    for line in sys.stdin:
        if not line.isspace():
            lines.append(line)
        else:
            break
    incidence_matrix = np.asarray(np.mat("".join(lines)))
    assert not graph.is_adjacency_matrix(incidence_matrix)
    colorized = coloring.welsh_powell(incidence_matrix)
    G = create_graph(incidence_matrix)
    colors = [colorized.get(v, 'blue') for v in G.nodes()]
    networkx.draw(
        G,
        with_labels=True,
        node_color=colors,
        edge_color='black',
        width=1,
        alpha=0.7)
    pyplot.show()
