import numpy as np


class Graph:
    def __init__(self, adjacency_matrix):
        self.adjacency_matrix = adjacency_matrix
        self.edges = []
        if adjacency_matrix.shape[0] != adjacency_matrix.shape[1]:
            raise IOError("Adjacency matrix should be square")
        for i in range(adjacency_matrix.shape[0]):
            for j in range(adjacency_matrix.shape[1]):
                if adjacency_matrix[i][j] != -1 and i != j:
                    self.edges.append([i, j, adjacency_matrix[i][j]])
        self._n = len(adjacency_matrix)
        self.distances = [[0]*self._n]

    def add_distances(self):
        possible_dists = [np.inf] * self._n
        last_dist = self.distances[-1]
        for edge in self.edges:
            possible_dists[edge[1]] = min(last_dist[edge[0]] + edge[2], possible_dists[edge[1]])
        self.distances.append(possible_dists)

    def get_pi_vect(self, l):
        if l >= len(self.distances):
            l_cur = len(self.distances)
            for _ in range(l - l_cur + 1):
                self.add_distances()
        return self.distances[l]

    def get_pi(self, l):
        return np.min(self.get_pi_vect(l))


