from typing import List


def adjacency_to_incidence(adj_matrix: List[List[int]]) -> List[List[int]]:
    """
    Converts an adjacency matrix to an incidence matrix.

    Parameters
    ----------
    adj_matrix : List[List[int]]
        The adjacency matrix of the graph.

    Returns
    -------
    List[List[int]]
        The incidence matrix of the graph, where each column represents an edge
        and each row corresponds to a vertex. The value is positive for the source
        vertex, negative for the target vertex, and zero otherwise.
    """

    n = len(adj_matrix)
    edges = []

    for i in range(n):
        for j in range(n):
            if adj_matrix[i][j] != 0:
                edges.append((i, j, adj_matrix[i][j]))

    m = len(edges)
    incidence_matrix = [[0] * m for _ in range(n)]

    for k, (i, j, w) in enumerate(edges):
        if i == j:
            incidence_matrix[i][k] = w
        else:
            incidence_matrix[i][k] = w
            incidence_matrix[j][k] = -w

    return incidence_matrix


def incidence_to_adjacency(incidence_matrix: List[List[int]]) -> List[List[int]]:
    """
    Converts an incidence matrix to an adjacency matrix.

    Parameters
    ----------
    incidence_matrix : List[List[int]]
        The incidence matrix of the graph, where each column represents an edge
        and each row corresponds to a vertex. The value is positive for the source
        vertex, negative for the target vertex, and zero otherwise.

    Returns
    -------
    List[List[int]]
        The adjacency matrix of the graph.
    """

    n = len(incidence_matrix)
    m = len(incidence_matrix[0]) if n > 0 else 0
    adj_matrix = [[0] * n for _ in range(n)]

    for k in range(m):
        source, target, weight = None, None, 0
        for i in range(n):
            if incidence_matrix[i][k] > 0:
                source = i
                weight = incidence_matrix[i][k]
            elif incidence_matrix[i][k] < 0:
                target = i

        if source is not None:
            target = target if target is not None else source
            adj_matrix[source][target] = weight

    return adj_matrix
