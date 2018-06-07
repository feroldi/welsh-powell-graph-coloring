import graph

def welsh_powell(G):
    """ Algoritmo de Welsh Powell: coloração de grafos em ordem decrescente.

    O algoritmo de Welsh Powell é um caso especial de um algoritmo guloso
    básico. O único adicional é a sugestão de uma ordem específica em que os
    vértices são visitados. A ideia é a seguinte: uma nova cor é necessária
    quando todos os vizinhos de um vértice já possuem as cores já criadas. Essa
    situação só ocorre para vértices de suficientemente alto grau, que são
    visitados após um número suficiente de deus vizinhos. Consequentemente, se
    tentarmos visitar primeiro os vértices graus maiores antes de seus
    vizinhos, o risco de precisar de uma nova cor deve diminuir.

    Os passos para o algoritmo são:

    1. Atribua a primeira cor para o primeiro vértice de maior grau.
    2. Para cada vértice restante de maior grau, colorize o vértice com a cor
       numerada mais baixa que não tenha sido usada por seus vizinhos ainda.
    """
    # É impossível colorizar grafos com laços.
    assert graph.is_simple_graph(G)
    # Contém os vértices numerados do grafo, em ordem decrescente baseado em
    # suas valências.
    vertices = list(range(graph.order(G)))
    vertices = sorted(vertices, key=lambda v: graph.vertex_degree(G, v), reverse=True)
    # Dicionário para guardar as cores usadas nos vértices.
    colorized = {}
    # Etapa 1: Atribua a primeira cor para o primeiro vértice de maior grau.
    colorized[vertices.pop(0)] = 0
    # Etapa 2: Percorre todos os vértices restantes e procura uma cor mínima
    # para pintá-los.
    for v in vertices:
        # Representa a disponibilidade de cada cor baseado no índice.
        available_colors = [True] * graph.order(G)
        # Percorre os vizinhos de `v` para checar se eles já estão colorizados.
        for adj_v in graph.adjacent_vertices(G, v):
            # Se um vizinho já está colorizado, marque sua cor como
            # indisponível.
            if adj_v in colorized:
                available_colors[colorized[adj_v]] = False
        # Coloriza o vértice `v` com a primeira cor disponível.
        for color, is_available in enumerate(available_colors):
            if is_available:
                colorized[v] = color
                break
    return colorized
