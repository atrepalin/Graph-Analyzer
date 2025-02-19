from lib.visualize import plot, Layout

adj_matrix = [[6, 4, 0, 0], [3, 0, 0, 7], [2, 9, 0, 0], [1, 0, 5, 0]]

# adj_matrix = [[0, 0, 0, 0], [3, 0, 0, 0], [2, 9, 0, 0], [1, 0, 5, 0]]

plot(adj_matrix, Layout.kamada_kawai)
