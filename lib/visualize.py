import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Tuple
from collections import defaultdict
from functools import partial
from enum import Enum
from .cycles import find_cycles, is_in_cycle, get_cycles_count


def adjacency_matrix_to_edge_list(
    adj_matrix: List[List[int]],
    cycles: List[List[int]] = [],
) -> List[Tuple[int, int, int]]:
    """
    Converts an adjacency matrix to a list of edges.

    Parameters
    ----------
    adj_matrix : List[List[int]]
        The adjacency matrix of the graph.
    cycles : List[List[int]], optional
        The cycles in the graph. If provided, an edge will be repeated as many times as it appears in a cycles.
        By default, each edge is only included once.

    Returns
    -------
    List[Tuple[int, int, int]]
        A list of edges in the format (source, target, weight), where an edge can appear
        in the list multiple times if it is part of multiple cycles.
    """
    edge_list = []
    num_vertices = len(adj_matrix)

    for i in range(num_vertices):
        for j in range(num_vertices):
            weight = adj_matrix[i][j]
            if weight != 0:
                # repeat the edge as many times as the number of cycles with it or just once

                count = get_cycles_count(i, j, cycles) or 1

                edge_list.extend([(i, j, weight)] * count)

    return edge_list


def edge_list_to_graph(edge_list: List[Tuple[int, int, int]]) -> nx.DiGraph:
    """
    Converts an edge list to a directed graph.

    Parameters
    ----------
    edge_list: List[Tuple[int, int, int]]
        A list of tuples where each tuple represents an edge in the format
        (source, target, weight).

    Returns
    -------
    nx.DiGraph
        A directed graph with edges added from the edge list, each with
        an associated weight.
    """

    G = nx.MultiDiGraph()

    for edge in edge_list:
        *edge, weight = edge

        G.add_edge(*edge, weight=weight)

    return G


colors = [
    "red",
    "blue",
    "green",
    "yellow",
    "orange",
    "purple",
    "pink",
    "brown",
    "grey",
    "cyan",
    "magenta",
    "violet",
    "teal",
    "maroon",
    "olive",
    "navy",
]


def get_color(edge: Tuple[int, int], cycles: List[List[int]], skip: int = 0) -> str:
    """
    Returns the color of the given edge in the graph.

    Parameters
    ----------
    edge : Tuple[int, int]
        The edge to be colored.
    cycles : List[List[int]]
        The list of cycles in the graph.
    skip : int
        The number of cycles to skip when checking the edge.

    Returns
    -------
    str
        The color of the edge.
    """
    if (idx := is_in_cycle(*edge, cycles, skip)) is not None:
        return colors[idx % len(colors)]
    else:
        return "black"


class Layout(Enum):
    shell = "shell"
    planar = "planar"
    random = "random"
    spiral = "spiral"
    spring = "spring"
    circular = "circular"
    spectral = "spectral"
    kamada_kawai = "kamada_kawai"
    fruchterman_reingold = "fruchterman_reingold"


layouts = {
    "shell": nx.shell_layout,
    "planar": nx.planar_layout,
    "random": nx.random_layout,
    "spiral": nx.spiral_layout,
    "spring": partial(nx.spring_layout, seed=0),
    "circular": nx.circular_layout,
    "spectral": nx.spectral_layout,
    "kamada_kawai": nx.kamada_kawai_layout,
    "fruchterman_reingold": partial(nx.fruchterman_reingold_layout, seed=0),
}


def plot_graph(
    G: nx.Graph, cycles: List[List[int]] = [], layout: Layout = Layout.shell
):
    """
    Plots the given graph with the given cycles.

    Parameters
    ----------
    G : nx.Graph
        The graph to be plotted.
    cycles : List[List[int]]
        The list of cycles in the graph.
    layout : Layout, optional
        The layout of the graph. Defaults to shell.

    Returns
    -------
    None
        The function does not return anything, it just plots the graph.
    """

    pos = layouts[layout.value](G)
    _, ax = plt.subplots(figsize=(8, 6))

    nx.draw_networkx_nodes(G, pos, ax=ax)

    # add node labels
    nx.draw_networkx_labels(
        G, pos, ax=ax, labels={n: f"X{n + 1}" for n in G.nodes()}, font_color="white"
    )

    # get self loop edges
    self_loop_edges = list(nx.selfloop_edges(G))

    # get non self loop edges
    edges = [edge for edge in G.edges() if edge not in self_loop_edges]

    # get edges which should be drawn curved
    # edges which are two way or occur more than once
    curved_edges = [
        edge
        for edge in edges
        if tuple(reversed(edge)) in edges or edges.count(edge) > 1
    ]

    # group edges by the number of times they occur
    curved_counts = defaultdict(list)

    for edge in curved_edges:
        count = edges.count(edge)

        curved_counts[count].append(edge)

    # get straight edges
    straight_edges = [edge for edge in edges if edge not in curved_edges]

    # draw edges
    nx.draw_networkx_edges(
        G,
        pos,
        ax=ax,
        edgelist=straight_edges,
        edge_color=[get_color(edge, cycles) for edge in straight_edges],
    )

    # draw self loop edges
    nx.draw_networkx_edges(
        G,
        pos,
        ax=ax,
        edgelist=self_loop_edges,
        edge_color=[get_color(edge, cycles) for edge in self_loop_edges],
    )

    # get edge weights
    edge_weights = nx.get_edge_attributes(G, "weight")

    # get weight of an edge
    def get_weight(edge: Tuple[int, int]) -> int:
        return edge_weights[(*edge, 0)]

    # draw curved edges with labels
    def draw_curved_edges(edges: List[Tuple[int, int]], i: int):
        # get radius for the arc
        rad = 0 if i == 1 else 0.2 + 0.1 * i

        nx.draw_networkx_edges(
            G,
            pos,
            ax=ax,
            edgelist=edges,
            connectionstyle=f"arc3, rad = {rad}",
            edge_color=[get_color(edge, cycles, i) for edge in edges],
        )

        # get edge labels
        curved_edge_labels = {edge: get_weight(edge) for edge in edges}

        # draw edge labels
        nx.draw_networkx_edge_labels(
            G, pos, ax=ax, edge_labels=curved_edge_labels, rotate=True
        )

    # draw curved edges based on the number of times they occur
    for count, edges in curved_counts.items():
        for i in range(count):
            # draw curved edges with labels for specific cycle by skipping other cycles
            draw_curved_edges(edges, i)

    # get edge labels
    straight_edge_labels = {edge: get_weight(edge) for edge in straight_edges}
    self_loop_edge_labels = {edge: get_weight(edge) for edge in self_loop_edges}

    # draw edge labels
    nx.draw_networkx_edge_labels(
        G, pos, ax=ax, edge_labels=straight_edge_labels, rotate=True
    )

    # draw self loop edge labels
    nx.draw_networkx_edge_labels(
        G, pos, ax=ax, edge_labels=self_loop_edge_labels, rotate=True
    )

    plt.show()


def plot(adj_matrix: List[List[int]], layout: Layout = Layout.shell):
    """
    Plots the graph represented by the given adjacency matrix.

    Parameters
    ----------
    adj_matrix : List[List[int]]
        The adjacency matrix of the graph.

    layout : Layout, optional
        The layout of the graph. Defaults to shell.

    Returns
    -------
    None
        The function does not return anything, it just plots the graph.
    """

    cycles = find_cycles(adj_matrix)

    edge_list = adjacency_matrix_to_edge_list(adj_matrix, cycles)

    G = edge_list_to_graph(edge_list)

    plot_graph(G, cycles, layout)
