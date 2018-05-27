#!/bin/env python
"""
Os grafos nesse programa são representados por uma matriz de incidência. Para
exemplificar os casos de grafos, entenda G(V, A) como sendo definido pelo par
de conjuntos V e A, onde:

    V é um conjunto não vazio dos vértices ou nodos do grafo;

    A é um conjunto de pares ordenados a=(v, w), v e w pertencentes a V: as
    arestas do grafo.

Numa matriz de incidência M, as linhas são nodos (v) e as colunas são arcos
(e), tal que M(i,j) = 1 se o vértice v(i) e o arco e(j) são incidente, e 0 caso
contrário. Para um digrafo (grafo assimétrico), M(i,j) = -1 se o arco e(j) sai
do vértice v(i), 1 se o arco e(j) chega no vértice v(i), e 0 caso contrário.
"""

import numpy as np
import itertools

# Ordem


def order(graph):
    """ A ordem de um grafo G é dada pela cardinalidade do conjunto de
    vértices, ou seja, pelo número de vértices de G. """
    rows, _ = graph.shape
    return rows


# Multigrafo


def loops(graph):
    """ Um laço é representado por uma coluna (arco) vazio, com apenas o
    elemento 2 em uma das linhas (vértice). Caso o elemento 2 não existir no
    grafo, então não temos laços presentes.

    Retorno: um iterador para a linha e coluna das posições dos laços.
    """
    if 2 in np.unique(graph):
        rows, cols = np.where(graph == 2)
        return zip(rows, cols)
    return zip()


def parallel_edges(graph):
    """ Arestas paralelas existem quando um vértice está ligado a outro por
    duas arestas ou mais.

    Gera uma sequência de pares de arcos que são paralelos (i.e. ligam dois
    vértices em comum).
    """
    for i, j in itertools.combinations(range(graph.shape[1]), 2):
        if np.array_equal(graph[:, i], graph[:, j]):
            yield i, j


def is_multigraph(graph):
    """ A definição de uma matriz de incidência aplica-se a grafos com laços e
    múltiplos arcos. """
    if 2 in np.unique(graph):
        return True
    for i, j in itertools.combinations(range(graph.shape[1]), 2):
        if np.array_equal(graph[:, i], graph[:, j]):
            return True
    return False


# Grafo simples


def is_simple_graph(graph):
    """ Um grafo simples não apresenta laços, nem arcos paralelos. Ou seja, não
    é um multigrafo. """
    return not is_multigraph(graph)


# Grafo trivial


def is_trivial_graph(graph):
    """ Um grafo trivial apresenta apenas um vértice com zero arestas. Ou seja,
    é um grafo vazio com apenas um vértice. """
    return graph.shape[0] == 1 and is_empty_graph(graph)


# Grafo vazio


def is_empty_graph(graph):
    """ Um grafo vazio é um grafo cujo conjunto de arestas é vazio. """
    return len(graph[graph != 0]) == 0


# Vértices adjacentes e Arestas adjacentes


def neighbours(graph, vertex):
    """ Procura pelos vértices adjacentes do vértice na posição `vertex` e
    retorna uma lista de pares (vértice vizinho, aresta conectada) """
    edges = graph[vertex]
    outgoing_edges, = np.where(edges > 0)
    for edge in outgoing_edges:
        link, = np.where(graph[:, edge] > 0)
        if len(link) == 2:
            yield (link[0] if link[0] != vertex else link[1]), edge
        else:
            # Em caso de laço, apenas um vértice é encontrado.
            yield link[0], edge


def adjacent_vertices(graph, vertex):
    """ Retorna um conjunto dos vértices que são adjacentes ao vértice `vertex`.
    """
    return {neighbour for neighbour, edge in neighbours(graph, vertex)}


def adjacent_edges(graph, vertex):
    """ Retorna um conjunto das arestas que são adjacentes ao vértice `vertex`.
    """
    return {edge for neighbour, edge in neighbours(graph, vertex)}


# Grafo completo


def is_complete_graph(graph):
    """ Um grafo completo é um grafo simples, onde o grau de todos os vértices
    é o mesmo. isto é, todos os vértices estão ligados uns aos outros por uma
    aresta direta. """
    if is_simple_graph(graph):
        for i, j in itertools.combinations(range(graph.shape[1]), 2):
            if vertex_degree(graph, i) != vertex_degree(graph, j):
                return False
        return True
    return False


# Grau


def vertex_degree(graph, vertex):
    """ O grau de um vértice em um grafo é a quantidade de arestas incidentes
    nesse vértice. Em um grafo não direcionado, um laço conta como duas arestas
    incidentes. """
    edges = graph[vertex]
    return edges[edges > 0].sum()


def vertex_indegree(graph, vertex):
    """ O grau de dentro de um vértice em um grafo é a quantidade de arestas
    que saem daquele vértice. """
    edges = graph[vertex]
    return np.count_nonzero(np.logical_or(edges == -1, edges == 2))


def vertex_outdegree(graph, vertex):
    """ O grau de fora de um vértice em um grafo é a quantidade de arestas
    incidentes nesse vértice. Em um grafo direcionado, um laço conta como
    apenas uma aresta incidentes. """
    edges = graph[vertex]
    return np.count_nonzero(np.logical_or(edges == 1, edges == 2))


# Reconhecimento de tipos de matrizes


def is_adjacency_matrix(graph):
    for i, j in itertools.combinations(range(graph.shape[1]), 2):
        if graph[i, j] != graph[j, i]:
            return False
    return True


# Matriz adjacente para matriz de incidência


def adjacency_to_incidence(adj_graph):
    assert is_adjacency_matrix(adj_graph)
    mat_length = len(adj_graph)
    incidence = []
    for row in range(mat_length):
        for col in range(row, mat_length):
            for _ in range(adj_graph[row, col]):
                edge = [0 for _ in range(mat_length)]
                edge[row] += 1
                edge[col] += 1
                incidence.append(edge)
    return np.array(incidence).T
