from typing import List, Tuple

INF = float("inf")


def floyd_warshall(
    adj_matrix: List[List[int]],
) -> Tuple[List[List[int]], List[List[int]]]:
    """
    Computes the shortest paths from every node to every other node in a weighted graph.

    Parameters
    ----------
    adj_matrix : List[List[int]]
        The adjacency matrix of the graph, where the value at position [u][v] is the
        weight of the edge from node u to node v.

    Returns
    -------
    Tuple[List[List[int]], List[List[int]]]
        A tuple of two lists, the first of which contains the shortest distances from
        every node to every other node, and the second of which contains the shortest
        paths from every node to every other node.
    """
    n = len(adj_matrix)

    for i in range(n):
        for j in range(n):
            if i != j and adj_matrix[i][j] == 0:
                adj_matrix[i][j] = INF

    dp = [[adj_matrix[i][j] for j in range(n)] for i in range(n)]
    paths = [[[] for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if adj_matrix[i][j] != INF and i != j:
                paths[i][j] = [i, j]
            elif i == j:
                paths[i][j] = [i]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dp[i][k] != INF and dp[k][j] != INF:
                    new_dist = dp[i][k] + dp[k][j]

                    if new_dist < dp[i][j]:
                        dp[i][j] = new_dist
                        paths[i][j] = paths[i][k] + paths[k][j][1:]

    return dp, paths
