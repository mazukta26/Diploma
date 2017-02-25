from Graph import Graph
import numpy as np
from unittest import TestCase


class TestGraph(TestCase):
    def test_init(self):
        adj_matr_with_loop = np.array([[1, 0, -1, -1],
                                       [-1, -1, 0, 0],
                                       [-1, 0, 1, 1],
                                       [-1, -1, -1, -1]])
        adj_matr_non_square = np.array([[1, 1, -1, -1, 1], [1, 0, -1, 0, 0]])
        caught = False
        try:
            _ = Graph(adj_matr_non_square)
        except IOError:
            caught = True
        else:
            pass
        if not caught:
            self.fail('Expected IOError')
        graph = Graph(adj_matr_with_loop)
        assert np.all(graph.adjacency_matrix == adj_matr_with_loop)
        assert graph._n == 4
        edges = [[0, 1, 0], [1, 2, 0], [1, 3, 0], [2, 1, 0], [2, 3, 1]]
        assert len(edges) == len(graph.edges) and all(edge in graph.edges for edge in edges)
        assert len(graph.distances) == 1 and graph.distances[0] == [0] * graph._n
        assert len(graph._from_vertice) == 1 and graph._from_vertice[0] == [0] * graph._n

    def test_add_distances(self):
        graph = Graph(np.array([[1, 0, -1, -1],
                                [-1, -1, 0, 0],
                                [-1, 1, 1, 1],
                                [-1, -1, 1, 0]]))
        graph.add_distances()
        dists1 = [np.inf, 0, 0, 0]
        vertices1 = [np.inf, 0, 1, 1]
        assert all(el1 == el2 for el1, el2 in zip(graph.distances[-1], dists1))
        assert all(el1 == el2 for el1, el2 in zip(graph._from_vertice[-1], vertices1))
        graph.add_distances()
        dists2 = [np.inf, 1, 0, 0]
        vertices2 = [np.inf, 2, 1, 1]
        assert all(el1 == el2 for el1, el2 in zip(graph.distances[-1], dists2))
        assert all(el1 == el2 for el1, el2 in zip(graph._from_vertice[-1], vertices2))
        graph.add_distances()
        dists3 = [np.inf, 1, 1, 1]
        vertices3 = [np.inf, 2, 1, 1]
        assert all(el1 == el2 for el1, el2 in zip(graph.distances[-1], dists3))
        assert all(el1 == el2 for el1, el2 in zip(graph._from_vertice[-1], vertices3))

    def test_get_pi_vect(self):
        graph = Graph(np.array([[1, 0, -1, -1],
                                [-1, -1, 0, 0],
                                [-1, 1, 1, 1],
                                [-1, -1, 1, 0]]))
        dists3 = [np.inf, 1, 1, 1]
        assert all(el1 == el2 for el1, el2 in zip(graph.get_pi_vect(3), dists3))
        dists2 = [np.inf, 1, 0, 0]
        assert all(el1 == el2 for el1, el2 in zip(graph.get_pi_vect(2), dists2))

    def test_get_pi(self):
        graph = Graph(np.array([[1, 0, -1, -1],
                                [-1, -1, 0, 0],
                                [-1, 1, 1, 1],
                                [-1, -1, 1, 0]]))
        assert graph.get_pi(3) == 1
        assert graph.get_pi(2) == 0

    def test_count_c(self):
        graph = Graph(np.array([[1, 0, -1, -1],
                                [-1, -1, 0, 0],
                                [-1, 1, 1, 1],
                                [-1, -1, 1, 0]]))
        assert 0.5 == graph.count_c()
        graph = Graph.read_graph_from_file('linear_trans')
        assert 0.5 == graph.count_c()
