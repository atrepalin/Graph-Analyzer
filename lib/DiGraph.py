from .cycles import find_cycles, convert_to_acyclic
from .graphics.visualize import plot as plot_graph, Layout
from .matrices import adjacency_to_incidence, incidence_to_adjacency
from .topo import is_topo_sorted, topo_sort
from .methods import shortest_paths_dp, dijkstra, floyd_warshall
from typing import List, Tuple


class DiGraph:
    """A class representing a directed graph."""

    adj_matrix: List[List[int]] = None
    cycles: List[List[int]] = None
    incidence_matrix: List[List[int]] = None
    is_topologically_sorted: bool = False

    def __init__(self, adj_matrix: List[List[int]]):
        """
        Initializes a new directed graph instance from an adjacency matrix.

        Parameters
        ----------
        adj_matrix : List[List[int]]
            The adjacency matrix of the graph, where a non-zero entry at position (u,v)
            indicates a directed edge from vertex u to vertex v.
        """
        self.adj_matrix = adj_matrix
        self.cycles = find_cycles(self.adj_matrix)
        self.incidence_matrix = adjacency_to_incidence(self.adj_matrix)
        self.is_topologically_sorted = is_topo_sorted(self.adj_matrix)

    @staticmethod
    def from_incidence(incidence_matrix: List[List[int]]) -> "DiGraph":
        """
        Creates a DiGraph from an incidence matrix.

        Parameters
        ----------
        incidence_matrix : List[List[int]]
            The incidence matrix of the graph, where each column represents an edge
            and each row corresponds to a vertex. The value is positive for the source
            vertex, negative for the target vertex, and zero otherwise.

        Returns
        -------
        DiGraph
            A new directed graph instance created from the given incidence matrix.
        """
        adj_matrix = incidence_to_adjacency(incidence_matrix)
        return DiGraph(adj_matrix)

    def make_acyclic(self) -> "DiGraph":
        """
        Makes the graph acyclic by removing the minimum number of edges to break all cycles.

        The resulting graph is a new instance of DiGraph, the original graph is not modified.

        Returns
        -------
        DiGraph
            The acyclic graph.
        """
        if len(self.cycles) == 0:
            return self

        return DiGraph(convert_to_acyclic(self.adj_matrix, self.cycles))

    def topological_sort(self) -> "DiGraph":
        """
        Performs a topological sort on the graph.

        This method rearranges the vertices of the graph in a linear ordering such that
        for every directed edge from vertex u to vertex v, u comes before v in the ordering.
        The graph must be acyclic to perform a topological sort.

        Returns
        -------
        DiGraph
            A new directed graph instance with vertices sorted in topological order.

        Raises
        ------
        Exception
            If the graph contains cycles, as a topological sort is not possible.
        """
        if len(self.cycles) > 0:
            raise Exception("Graph is not acyclic")
        if self.is_topologically_sorted:
            return self

        return DiGraph(topo_sort(self.adj_matrix))

    def shortest_path_dp(self, source: int) -> Tuple[List[float], List[List[int]]]:
        """
        Computes the shortest paths from a source node to all other nodes in a weighted graph.

        This algorithm assumes that the graph is topologically sorted. If the graph is not
        topologically sorted, it will raise an exception.

        Parameters
        ----------
        source : int
            The index of the source node.

        Returns
        -------
        Tuple[List[float], List[List[int]]]
            A tuple of two lists, the first of which contains the shortest distances from
            the source node to all other nodes, and the second of which contains the shortest
            paths from the source node to all other nodes.
        """
        if not self.is_topologically_sorted:
            raise Exception("Graph is not topologically sorted")

        return shortest_paths_dp(self.adj_matrix, source)

    def shortest_path_dijkstra(
        self, source: int
    ) -> Tuple[List[float], List[List[int]]]:
        """
        Computes the shortest paths from a source node to all other nodes in a weighted graph.

        This function uses Dijkstra's algorithm to calculate the shortest paths from the source node
        to all other nodes in the graph. The graph must be a simple weighted graph.

        Parameters
        ----------
        source : int
            The index of the source node.

        Returns
        -------
        Tuple[List[float], List[List[int]]]
            A tuple of two lists, the first of which contains the shortest distances from
            the source node to all other nodes, and the second of which contains the shortest
            paths from the source node to all other nodes.
        """
        return dijkstra(self.adj_matrix, source)

    def shortest_path_floyd_warshall(self) -> Tuple[List[float], List[List[int]]]:
        """
        Computes the shortest paths from every node to every other node in a weighted graph.

        This function uses the Floyd-Warshall algorithm to calculate the shortest paths from
        every node to every other node in the graph. The graph must be a simple weighted graph.

        Returns
        -------
        Tuple[List[float], List[List[int]]]
            A tuple of two lists, the first of which contains the shortest distances from
            every node to every other node, and the second of which contains the shortest
            paths from every node to every other node.
        """
        return floyd_warshall(self.adj_matrix)

    def print(self):
        """
        Prints the details of the directed graph.

        This includes the adjacency matrix, incidence matrix, cycles (if any),
        and whether the graph is topologically sorted.
        """
        print("=============== DiGraph ==============")
        print("Adjacency matrix:")
        print(*self.adj_matrix, sep="\n")
        print("Incidence matrix:")
        print(*self.incidence_matrix, sep="\n")
        if self.cycles:
            print("Cycles:")
            print(*self.cycles, sep="\n")
        print("Is topologically sorted:", self.is_topologically_sorted)

    def plot(self, layout: Layout = Layout.shell):
        """
        Plots the graph represented by the given adjacency matrix.

        Parameters
        ----------
        layout : Layout, optional
            The layout of the graph. Defaults to shell.

        Returns
        -------
        None
            The function does not return anything, it just plots the graph.
        """

        plot_graph(self.adj_matrix, layout)
