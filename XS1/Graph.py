import sys
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
        self.cycles, self.weights = [], []

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
        if len(self.weights) > 0:
            return np.min(self.weights)
        number_of_steps = self._n * 2
        pi_vect = self.get_pi_vect(number_of_steps)
        cycles, weights = [], []
        for i in range(self._n):
            if np.isfinite(pi_vect[i]):
                step, new_cycle, new_cycle_dict, this_vertice = number_of_steps, [], dict(), i
                while this_vertice not in new_cycle_dict:
                    new_cycle.append(this_vertice)
                    new_cycle_dict[this_vertice] = step
                    this_vertice = self._from_vertice[step][this_vertice]
                    step -= 1
                weight = self.distances[new_cycle_dict[this_vertice]][this_vertice] - self.distances[step][this_vertice]
                weights.append(weight * 1.0 / (new_cycle_dict[this_vertice] - step))
                cycles.append(new_cycle + [this_vertice])
        self.cycles = cycles
        self.weights = weights
        return np.min(weights)

    @staticmethod
    def read_graph_from_file(filename):
        file_lines = open(filename, 'r').readlines()
        adjacency_matrix = np.array([list(map(lambda x: int(x.strip()), line.split(","))) for line in file_lines])
        return Graph(adjacency_matrix)


if __name__ == '__main__':
    graph_filename = sys.argv[1]
    graph = Graph.read_graph_from_file(graph_filename)
    print("MCM is equal to {}".format(graph.count_c()))






