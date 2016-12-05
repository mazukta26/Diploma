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
        self._from_vertice = [[0] * self._n]

    def add_distances(self):
        possible_dists = [np.inf] * self._n
        from_vertice = [np.inf] * self._n
        last_dist = self.distances[-1]
        for edge in self.edges:
            if last_dist[edge[0]] + edge[2] < possible_dists[edge[1]]:
                possible_dists[edge[1]] = last_dist[edge[0]] + edge[2]
                from_vertice[edge[1]] = edge[0]
        self.distances.append(possible_dists)
        self._from_vertice.append(from_vertice)

    def get_pi_vect(self, l):
        if l >= len(self.distances):
            l_cur = len(self.distances)
            for _ in range(l - l_cur + 1):
                self.add_distances()
        return self.distances[l]

    def get_pi(self, l):
        return np.min(self.get_pi_vect(l))

    def count_c(self):
        cycle_el = np.argmin(self.get_pi_vect(self._n * 2))
        min_cycle_vertices = set()
        last_step_index = len(self._from_vertice) - 1
        cycle = []
        while cycle_el not in min_cycle_vertices:
            cycle.append(cycle_el)
            min_cycle_vertices.add(cycle_el)
            cycle_el = self._from_vertice[last_step_index][cycle_el]
            last_step_index -= 1
        cycle_weight = self.get_pi(2 * self._n) - self.get_pi(last_step_index)
        return cycle_weight / len(cycle)



