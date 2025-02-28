from typing import List, Tuple

INF = float("inf")


def bellman_ford(
    adj_matrix: List[List[int]], source: int
) -> Tuple[List[float], List[List[int]]]:
    """
    Computes the shortest paths from a source node to all other nodes in a weighted graph.

    The algorithm iterates over all edges in the graph at most n-1 times, where n is the
    number of vertices in the graph. On the i-th iteration, it relaxes all edges such that
    the minimum distance from the source node to all other nodes is reduced to the minimum
    possible value. The algorithm terminates when no more updates can be made.

    If the graph contains a negative cycle, the algorithm detects it and returns None.

    Parameters
    ----------
    adj_matrix : List[List[int]]
        The adjacency matrix of the graph, where the value at position (u,v) is the
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

    edges = []
    for i in range(n):
        for j in range(n):
            if i != j and adj_matrix[i][j] != 0:
                edges.append((i, j, adj_matrix[i][j]))

    dp = [INF] * n
    dp[source] = 0
    paths = [[] for _ in range(n)]
    paths[source] = [[source]]

    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dp[u] != INF and dp[u] + w < dp[v]:
                dp[v] = dp[u] + w
                paths[v] = [path + [v] for path in paths[u]]
                updated = True

        if not updated:
            break

    for u, v, w in edges:
        if dp[u] != INF and dp[u] + w < dp[v]:
            return None, None

    return dp, paths
