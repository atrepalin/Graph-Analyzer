from .cycles import find_cycles, convert_to_acyclic
from .graphics.visualize import plot as plot_graph, Layout
from .matrices import adjacency_to_incidence, incidence_to_adjacency
from .topo import is_topo_sorted, topo_sort
from .methods import shortest_paths_dp, dijkstra
from typing import List, Tuple


class DiGraph:
    adj_matrix: List[List[int]] = None
    cycles: List[List[int]] = None
    incidence_matrix: List[List[int]] = None
    is_topologically_sorted = False

    def __init__(self, adj_matrix: List[List[int]]):
        self.adj_matrix = adj_matrix
        self.cycles = find_cycles(self.adj_matrix)
        self.incidence_matrix = adjacency_to_incidence(self.adj_matrix)
        self.is_topologically_sorted = is_topo_sorted(self.adj_matrix)

    @staticmethod
    def from_incidence(incidence_matrix: List[List[int]]):
        adj_matrix = incidence_to_adjacency(incidence_matrix)
        return DiGraph(adj_matrix)

    def make_acyclic(self) -> "DiGraph":
        if len(self.cycles) == 0:
            return self

        return DiGraph(convert_to_acyclic(self.adj_matrix))

    def topological_sort(self) -> "DiGraph":
        if len(self.cycles) > 0:
            raise Exception("Graph is not acyclic")
        if self.is_topologically_sorted:
            return self

        return DiGraph(topo_sort(self.adj_matrix))

    def plot(self, layout: Layout = Layout.shell):
        plot_graph(self.adj_matrix, layout)

    def shortest_path_dp(self, source: int) -> Tuple[List[float], List[List[int]]]:
        if not self.is_topologically_sorted:
            raise Exception("Graph is not topologically sorted")
        return shortest_paths_dp(self.adj_matrix, source)

    def shortest_path_dijkstra(
        self, source: int
    ) -> Tuple[List[float], List[List[int]]]:
        return dijkstra(self.adj_matrix, source)

    def print(self):
        print("=============== DiGraph ==============")
        print("Adjacency matrix:")
        print(*self.adj_matrix, sep="\n")
        print("Incidence matrix:")
        print(*self.incidence_matrix, sep="\n")
        if self.cycles:
            print("Cycles:")
            print(*self.cycles, sep="\n")
        print("Is topologically sorted:", self.is_topologically_sorted)
