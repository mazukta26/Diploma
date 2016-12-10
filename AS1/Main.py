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
    print(a)
    print(b)
    return a, b


if __name__ == '__main__':
    as1 = AS1(*create_belt(8))
    t1 = time()
    lin = as1.create_linear_transitions_graph()
    print("Time", time()-t1)
    t1 = time()
    diff = as1.create_differential_graph()
    print("Time", time()-t1)
    t1 = time()
    l_graph = Graph(lin)
    d_graph = Graph(diff)
    print("Time", time() - t1)
    t1 = time()
    print(l_graph.count_c())
    print("Time", time() - t1)
    t1 = time()
    print(d_graph.count_c())
    print("Time", time() - t1)
    t1 = time()
