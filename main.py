import argparse
import sys
import numpy as np
import graph

parser = argparse.ArgumentParser(description='Classificador de grafos')
parser.add_argument(
    '-',
    dest='read_from_stdin',
    action='store_true',
    help='matrizes são lidas pela entrada padrão')
args = parser.parse_args()


def interactive_input_matrices():
    def input_matrix():
        # Entra com uma dimensão e uma matriz.
        rows, cols = input('Dimensão da matriz MxN: ').split('x')
        rows, cols = int(rows), int(cols)
        matrix = [
            int(input(f'Posição [{i},{j}]: ')) for i in range(rows)
            for j in range(cols)
        ]
        return np.reshape(matrix, (rows, cols))

    print('Matriz de adjacência')
    adj_mat = input_matrix()
    if not graph.is_adjacency_matrix(adj_mat):
        raise RuntimeError(
            'Matriz de adjacência entrada não é uma matriz de adjacência')
    print('Matriz de incidência')
    inc_mat = input_matrix()
    if graph.is_adjacency_matrix(inc_mat):
        raise RuntimeError(
            'Matriz de incidência entrada não é uma matriz de incidência')
    return adj_mat, inc_mat


def automated_input_matrices():
    def input_matrix():
        # Analisa as matrizes com a função `np.mat` e passa elas para
        # `np.array`s.
        lines = []
        for line in sys.stdin:
            if not line.isspace():
                lines.append(line)
            else:
                break
        return np.asarray(np.mat("".join(lines)))

    adj_mat = input_matrix()
    inc_mat = input_matrix()
    assert graph.is_adjacency_matrix(adj_mat)
    assert not graph.is_adjacency_matrix(inc_mat)
    return adj_mat, inc_mat


def error_on_differing_matrices(adjacency_mat, incidence_mat):
    inc_from_adj_mat = graph.adjacency_to_incidence(adjacency_mat)
    if np.any(inc_from_adj_mat != incidence_mat):
        raise RuntimeError(
            'Matriz de adjacência não é equivalente a matriz de incidência')


def output_graph_properties(G):
    print(f'ordem: {graph.order(G)}')
    print(f'multigrafo: {graph.is_multigraph(G)}')
    print(f'grafo simples: {graph.is_simple_graph(G)}')
    print(f'grafo trivial: {graph.is_trivial_graph(G)}')
    print(f'grafo vazio: {graph.is_empty_graph(G)}')
    print(f'grafo completo: {graph.is_complete_graph(G)}')
    for v in range(graph.order(G)):
        vertices = graph.adjacent_vertices(G, v)
        print(f'vértices adjacentes do vértice {v}: {vertices}')
    for v in range(graph.order(G)):
        edges = graph.adjacent_edges(G, v)
        print(f'arestas adjacentes do vértice {v}: {edges}')


if __name__ == '__main__':
    if args.read_from_stdin:
        adj, inc = automated_input_matrices()
    else:
        adj, inc = interactive_input_matrices()
    error_on_differing_matrices(adj, inc)
    output_graph_properties(inc)
