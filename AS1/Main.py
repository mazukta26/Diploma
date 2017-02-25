import numpy as np
from AS1 import AS1
from Graph import Graph
from time import time


def create_belt(n):
    a = [1] * (n-1) + [0]
    b = np.zeros((n, n+1))
    for i in range(n-1):
        b[i][i+1] = 1
    b[-2, -1] = 1
    b[-1, :-2] = 1
    # print(a)
    # print(b)
    return a, b


if __name__ == '__main__':
    for n in range(2, 20):
        as1 = AS1(*create_belt(n))
        lin = as1.create_linear_transitions_graph()
        diff = as1.create_differential_graph()
        l_graph = Graph(lin)
        d_graph = Graph(diff)
        print("lambda({}) = {}".format(n, l_graph.count_c()))
        print("pi({}) = {}".format(n, d_graph.count_c()))
