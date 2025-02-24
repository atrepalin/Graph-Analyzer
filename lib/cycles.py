from typing import List, Set
from copy import deepcopy

def shift(arr: List[int], n: int) -> List[int]:
    """
    Shifts the elements of the list by n positions.

    Args:
        arr (List[int]): The list of integers to be shifted.
        n (int): The number of positions to shift the list.

    Returns:
        List[int]: A new list with elements shifted by n positions.
    """

    return arr[-n:] + arr[:-n]


def find_cycles(adj_matrix: List[List[int]]) -> List[List[int]]:
    """
    Finds all unique cycles in a graph represented by an adjacency matrix.

    This function uses a depth-first search (DFS) approach to identify all cycles
    in the graph. A cycle is a path that starts and ends at the same node and does
    not repeat any nodes except the starting and ending node. The detected cycles
    are unique.

    Args:
        adj_matrix (List[List[int]]): The adjacency matrix of the graph, where
            each element indicates the presence (1) or absence (0) of an edge.

    Returns:
        List[List[int]]: A list of cycles, where each cycle is represented as a list
        of node indices. The cycles are closed with the starting node appended at
        the end of each cycle.
    """

    def dfs(node: int, start: int, visited: List[int], stack: Set[int]):
        """
        A helper function to perform a depth-first search (DFS) for finding cycles
        in a graph.

        Args:
            node (int): The current node being visited.
            start (int): The starting node of the cycle.
            visited (List[int]): A list of visited nodes.
            stack (Set[int]): A set of nodes in the current stack.

        Returns:
            None
        """
        if node in stack:
            if node == start:
                cycle = visited[:]

                for i in range(len(cycle)):
                    if shift(cycle, i) in cycles:
                        return
                else:
                    cycles.append(cycle)

            return

        if node in visited:
            return

        stack.add(node)
        visited.append(node)

        for neighbor, has_edge in enumerate(adj_matrix[node]):
            if has_edge:
                dfs(neighbor, start, visited.copy(), stack.copy())

    cycles = []
    for start_node in range(len(adj_matrix)):
        dfs(start_node, start_node, [], set())

    return list(map(lambda cycle: cycle + [cycle[0]], cycles))


def is_in_cycle(S: int, F: int, cycles: List[List[int]], skip: int) -> int:
    """
    Checks if an edge is in a cycle and returns its index if it is. Skip is the number
    of cycles to skip when checking the edge.

    Parameters
    ----------
    S : int
        The source of the edge.
    F : int
        The finish of the edge.
    cycles : List[List[int]]
        The list of cycles.
    skip : int
        The number of cycles to skip when checking the edge.

    Returns
    -------
    int
        The index of the cycle the edge is in if it is, None otherwise.
    """

    for idx, cycle in enumerate(cycles):
        for i in range(len(cycle) - 1):
            if cycle[i] == S and cycle[i + 1] == F:
                if skip == 0:
                    return idx

                skip -= 1

    return None


def get_cycles_count(S: int, F: int, cycles: List[List[int]]) -> int:
    """
    Gets the number of cycles an edge is in.

    Parameters
    ----------
    S : int
        The source of the edge.
    F : int
        The finish of the edge.
    cycles : List[List[int]]
        The list of cycles.

    Returns
    -------
    int
        The number of cycles the edge is in.
    """

    count = 0

    for cycle in cycles:
        for i in range(len(cycle) - 1):
            if cycle[i] == S and cycle[i + 1] == F:
                count += 1

    return count

def remove_min_edges_to_acyclic(adj_matrix, cycles):
    from collections import defaultdict

    edge_counts = defaultdict(int)
    
    for cycle in cycles:
        for i in range(len(cycle) - 1):
            edge = (cycle[i], cycle[i + 1])
            edge_counts[edge] += 1
    
    graph = {i: set() for i in range(len(adj_matrix))}
    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix)):
            if adj_matrix[i][j]:
                graph[i].add(j)
    
    def find_cycles():
        cycles_found = []
        path = []
        visited = set()

        def dfs(node):
            if node in path:
                cycle_start = path.index(node)
                cycles_found.append(path[cycle_start:] + [node])
                return
            if node in visited:
                return
            
            path.append(node)
            visited.add(node)
            for neighbor in graph[node]:
                dfs(neighbor)
            path.pop()
        
        for v in graph:
            dfs(v)
        return cycles_found
    
    removed_edges = set()
    while find_cycles():
        edge_to_remove = max(edge_counts, key=edge_counts.get)
        removed_edges.add(edge_to_remove)
        graph[edge_to_remove[0]].remove(edge_to_remove[1])
        del edge_counts[edge_to_remove]
    
    return removed_edges

def remove_edges_from_matrix(adj_matrix, removed_edges):
    adj_matrix = deepcopy(adj_matrix)

    for v, u in removed_edges:
        adj_matrix[v][u] = 0

    return adj_matrix