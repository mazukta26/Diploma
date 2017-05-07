import os
import sys
import numpy as np
from XS1 import XS1
from Graph import Graph
from time import time


def create_belt(n):
    a = [1] * (n - 1) + [0]
    b = np.zeros((n, n + 1))
    for i in range(n - 1):
        b[i][i + 1] = 1
    b[-2, -1] = 1
    b[-1, :-2] = 1
    return a, b


def parse_graph(adj_matrix, name):
    graph = Graph(adj_matrix)
    print("Characteristics for {}, graph size is {}:".format(name, graph._n))
    print("MCM characteristic: {}".format(graph.count_c()))
    # for i in range(1, graph._n*100+1):
    #     print("Pi({}) = {}".format(i, graph.get_pi(i)))
    print("Pi({}) = {}; Ratio: {}".format(graph._n * 100, graph.get_pi(graph._n * 100),
                                          graph.get_pi(graph._n * 100) / (graph._n * 100)))


def print_report_for_every_scheme():
    directory = "/home/svetlana/Diploma_Agievich/xs/data/"
    for scheme in os.listdir(directory):
        if os.path.isfile(directory + scheme):
            print(scheme.capitalize())
            xs = XS1.read_from_file(directory + scheme, " ")
            parse_graph(xs.create_linear_transitions_graph(), "Linear transition graph")
            parse_graph(xs.create_differential_graph(), "Differential graph")
            print()


if __name__ == '__main__':
    for n in range(2, 16):
        t = time()
        xs1 = XS1(*create_belt(n))
        lin = xs1.create_linear_transitions_graph()
        diff = xs1.create_differential_graph()
        l_graph = Graph(lin)
        d_graph = Graph(diff)
        print("lambda({}) = {}".format(n, l_graph.count_c()))
        print("pi({}) = {}".format(n, d_graph.count_c()))
        print(time() - t)
