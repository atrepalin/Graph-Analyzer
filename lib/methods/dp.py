from typing import List, Tuple

INF = float("inf")


def shortest_paths_dp(
    adj_matrix: List[List[int]], source: int
) -> Tuple[List[float], List[List[int]]]:
    """
    Computes the shortest paths from a source node to all other nodes in a weighted graph.

    Parameters
    ----------
    adj_matrix : List[List[int]]
        The adjacency matrix of the graph, where the value at position [u][v] is the
        weight of the edge from node u to node v.
    source : int
        The index of the source node.

    Returns
    -------
    Tuple[List[float], List[List[int]]]
        A tuple of two lists, the first of which contains the shortest distances from
        the source node to all other nodes, and the second of which contains the shortest
        paths from the source node to all other nodes.
    """

    n = len(adj_matrix)

    dp = [INF] * n
    dp[source] = 0
    paths = [[] for _ in range(n)]
    paths[source] = [[source]]

    for u in range(n):
        if dp[u] == INF:
            continue

        for v in range(n):
            if adj_matrix[u][v] != 0:
                new_dist = dp[u] + adj_matrix[u][v]

                if new_dist < dp[v]:
                    dp[v] = new_dist
                    paths[v] = [path + [v] for path in paths[u]]
                elif new_dist == dp[v]:
                    paths[v].extend([path + [v] for path in paths[u]])

    return dp, paths
