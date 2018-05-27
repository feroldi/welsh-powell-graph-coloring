import numpy as np
import graph


def test_adjacency_to_incidence():
    # Grafo com laços.
    adj = np.array([[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 1]])
    inc = np.array([[1, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 1, 2]])
    assert graph.is_adjacency_matrix(adj)
    assert not graph.is_adjacency_matrix(inc)

    conversion = graph.adjacency_to_incidence(adj)
    assert not graph.is_adjacency_matrix(conversion)
    assert np.all(inc == conversion)

    # Grafo com arestas paralelas
    adj = np.array([[0, 1, 2, 0], [1, 0, 0, 1], [2, 0, 0, 0], [0, 1, 0, 1]])
    inc = np.array([[1, 1, 1, 0, 0], [1, 0, 0, 1, 0], [0, 1, 1, 0, 0],
                    [0, 0, 0, 1, 2]])
    assert np.all(inc == graph.adjacency_to_incidence(adj))


def test_order():
    mat = np.array([[1, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 1, 2]])
    assert 4 == graph.order(mat)


def test_loops():
    mat_with_loop = np.array([[1, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 0],
                              [0, 0, 1, 2]])
    assert [(3, 3)] == list(graph.loops(mat_with_loop))

    mat_without_loop = np.array([[1, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 0],
                                 [0, 0, 1, 0]])
    assert [] == list(graph.loops(mat_without_loop))


def test_parallel_edges():
    # Grafo com duas arestas paralelas.
    mat1 = np.array([[1, 1, 1, 0, 0], [1, 0, 0, 1, 0], [0, 1, 1, 0, 0],
                     [0, 0, 0, 1, 2]])
    assert [(1, 2)] == list(graph.parallel_edges(mat1))

    # Grafo com pares de arestas paralelas.
    mat2 = np.array([[1, 1, 1, 1, 1], [1, 0, 0, 1, 0], [0, 1, 1, 0, 1]])
    assert [(0, 3), (1, 2), (1, 4), (2, 4)] == list(graph.parallel_edges(mat2))

    # Grafo sem arestas paralelas.
    mat3 = np.array([[1, 1, 1, 0], [1, 0, 0, 0], [0, 1, 0, 1], [0, 0, 1, 1]])
    assert graph.is_simple_graph(mat3)
    assert [] == list(graph.parallel_edges(mat3))


def test_multigraph():
    # Grafo com laços.
    mat_with_loops = np.array([[1, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 0],
                               [0, 0, 1, 2]])
    assert graph.is_multigraph(mat_with_loops)
    assert not graph.is_simple_graph(mat_with_loops)

    # Grafo com arestas paralelas.
    mat_with_parallel_edges = np.array([[1, 1, 1, 0, 0], [1, 0, 0, 1, 0],
                                        [0, 1, 1, 0, 0], [0, 0, 0, 1, 2]])
    assert graph.is_multigraph(mat_with_parallel_edges)
    assert not graph.is_simple_graph(mat_with_parallel_edges)

    # Grafo simples
    mat_simple = np.array([[1, 1, 1, 0], [1, 0, 0, 0], [0, 1, 0, 1],
                           [0, 0, 1, 1]])
    assert not graph.is_multigraph(mat_simple)
    assert graph.is_simple_graph(mat_simple)


def test_trivial_graph():
    trivial = np.array([[0, 0]])
    assert graph.is_trivial_graph(trivial)

    nontrivial = np.array([[0, 1], [1, 1], [1, 0]])
    assert not graph.is_trivial_graph(nontrivial)


def test_empty_graph():
    empty = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    assert graph.is_empty_graph(empty)

    empty2 = np.array([[]])
    assert graph.is_empty_graph(empty2)

    nonempty = np.array([[0, 1, 0], [0, 0, 0], [0, 1, 0]])
    assert not graph.is_empty_graph(nonempty)


def test_neighbour_vertices():
    mat = np.array([[1, 1, 1, 0, 0], [1, 0, 0, 1, 0], [0, 1, 1, 0, 0],
                    [0, 0, 0, 1, 2]])
    assert [(1, 0), (2, 1), (2, 2)] == list(graph.neighbours(mat, 0))
    assert [(0, 0), (3, 3)] == list(graph.neighbours(mat, 1))
    assert [(0, 1), (0, 2)] == list(graph.neighbours(mat, 2))
    assert [(1, 3), (3, 4)] == list(graph.neighbours(mat, 3))


def test_complete_graph():
    noncomplete = np.array([[1, 1, 1, 0, 0], [1, 0, 0, 1, 0], [0, 1, 1, 0, 0],
                            [0, 0, 0, 1, 2]])
    assert not graph.is_complete_graph(noncomplete)

    noncomplete = np.array([[1, 0, 0], [1, 1, 0], [0, 1, 0]])
    assert not graph.is_complete_graph(noncomplete)

    complete = np.array([[1, 0, 1], [1, 1, 0], [0, 1, 1]])
    assert graph.is_complete_graph(complete)

    complete = np.array([[1], [1]])
    assert graph.is_complete_graph(complete)

    complete = np.array([[0], [0]])
    assert graph.is_complete_graph(complete)


def test_vertex_degree():
    mat = np.array([[1, 1, 1, 0, 0], [1, 0, 0, 1, 0], [0, 1, 1, 0, 0],
                    [0, 0, 0, 1, 2]])
    assert 3 == graph.vertex_degree(mat, 0)
    assert 2 == graph.vertex_degree(mat, 1)
    assert 2 == graph.vertex_degree(mat, 2)
    assert 3 == graph.vertex_degree(mat, 3)  # Laços contam como dois.

    mat = np.array([[-1, 1, 1, 0, 0], [1, 0, 0, -1, 0], [0, -1, 1, 0, 0],
                    [0, 0, 0, 1, 2]])
    assert 2 == graph.vertex_outdegree(mat, 0)
    assert 1 == graph.vertex_outdegree(mat, 1)
    assert 1 == graph.vertex_outdegree(mat, 2)
    assert 2 == graph.vertex_outdegree(mat, 3)  # Laços contam como um.

    assert 1 == graph.vertex_indegree(mat, 0)
    assert 1 == graph.vertex_indegree(mat, 1)
    assert 1 == graph.vertex_indegree(mat, 2)
    assert 1 == graph.vertex_indegree(mat, 3)  # Laços contam como um.
