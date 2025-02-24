from typing import List
from collections import deque

def is_topo_sorted(adj_matrix: List[List[int]]) -> bool:
    """Checks if the given adjacency matrix is topologically sorted.

    A topological ordering of a directed acyclic graph (DAG) is a linear ordering
    of its vertices such that for every directed edge uv from vertex u to vertex v,
    u comes before v in the ordering.

    The function checks if the given adjacency matrix represents a topological
    ordering of the graph by checking if there are any edges from a vertex to a
    vertex with a lower index.

    Parameters
    ----------
    adj_matrix : List[List[int]]
        The adjacency matrix of the graph.

    Returns
    -------
    bool
        True if the graph is topologically sorted, False otherwise.
    """
    n = len(adj_matrix)
    for i in range(n):
        for j in range(i):
            if adj_matrix[i][j] != 0:
                return False
            
    return True

def topo_sort_order(adj_matrix: List[List[int]]) -> List[int]:
    """
    Computes a topological order of the vertices in a directed acyclic graph (DAG).

    This function uses Kahn's algorithm to determine a topological ordering of the graph
    represented by the given adjacency matrix. It calculates the in-degrees of all vertices,
    then iteratively removes vertices with in-degree zero, appending them to the topological
    order list, and decreasing the in-degree of their neighbors.

    Parameters
    ----------
    adj_matrix : List[List[int]]
        The adjacency matrix of the graph, where a non-zero entry at position (u,v) indicates
        a directed edge from vertex u to vertex v.

    Returns
    -------
    List[int]
        A list of vertices representing a topological ordering of the graph, or None if the graph
        contains a cycle.
    """

    n = len(adj_matrix)
    in_degree = [0] * n
    
    for u in range(n):
        for v in range(n):
            if adj_matrix[u][v] != 0:
                in_degree[v] += 1

    queue = deque([i for i in range(n) if in_degree[i] == 0])
    topo_order = []

    while queue:
        u = queue.popleft()
        topo_order.append(u)
        for v in range(n):
            if adj_matrix[u][v] != 0:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

    return topo_order if len(topo_order) == n else None

def rearrange_adj_matrix(adj_matrix: List[List[int]], topo_order: List[int]) -> List[List[int]]:
    """
    Rearranges the given adjacency matrix according to the given topological order.

    Parameters
    ----------
    adj_matrix : List[List[int]]
        The adjacency matrix of the graph.
    topo_order : List[int]
        A list of vertices representing a topological ordering of the graph.

    Returns
    -------
    List[List[int]]
        The rearranged adjacency matrix.
    """
    
    n = len(adj_matrix)
    sorted_matrix = [[0] * n for _ in range(n)]

    index_map = {topo_order[i]: i for i in range(n)}

    for i in range(n):
        for j in range(n):
            sorted_matrix[index_map[i]][index_map[j]] = adj_matrix[i][j]

    return sorted_matrix

def topo_sort(adj_matrix: List[List[int]]) -> List[List[int]]:
    """
    Computes a topological ordering of the vertices in a directed acyclic graph (DAG) and returns the
    rearranged adjacency matrix.

    Parameters
    ----------
    adj_matrix : List[List[int]]
        The adjacency matrix of the graph, where a non-zero entry at position (u,v) indicates
        a directed edge from vertex u to vertex v.

    Returns
    -------
    List[List[int]]
        The rearranged adjacency matrix, where the rows and columns are sorted according to a topological
        ordering of the graph.
    """
    topo_order = topo_sort_order(adj_matrix)
    sorted_matrix = rearrange_adj_matrix(adj_matrix, topo_order)
    return sorted_matrix