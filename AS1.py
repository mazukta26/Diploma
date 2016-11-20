import numpy as np
import matplotlib

def get_int(bool_arr):
    res = 0
    for bit in bool_arr:
        res *= 2
        res += bit
    return res

def get_bool(num, n):
    res = []
    while num > 0:
        res.append(num % 2)
        num //= 2
    res += [0] * (n - len(res))
    return res[::-1]

def diff_oper(operands):
    if np.all(operands == [0] ):
        return (0,)
    if np.sum(operands) == 1:
        return (1,)
    return (0,1)

def get_transitions(a,b,v):
    print v
    s = np.sum(a*v)
    v.append(s)
    trans = []
    for row in b:
        trans.append(diff_oper(row*v))
    res = []
    for el in trans[0]:
        res.append([el])
    for tran in trans[1:]:
        l = len(res)
        res = res*len(tran)
        for i,el in enumerate(tran):
            for j in range(l):
                res[i*l+j].append(el)
    return res, s


def create_differential_graph(a,b):
    n = len(a)
    graph = np.full((2**n,2**n), fill_value = -1, dtype = 'int64')
    for i in range(2**n):
        v = get_bool(i, n)
        all_transitions, their_s = get_transitions(a,b,v)
        for trans in all_transitions:
            graph[i, get_int(trans)] = their_s
    return graph

a = []
b = []
with open("as", 'r') as inp:
    lines = inp.readlines()
    lines = [line.strip() for line in lines if line.strip()]
    a = map(int, lines[0].split(","))
    b = [map(int, line.split(",")) for line in lines[1:]]
a = np.array(a)
b = np.array(b)
print a, b

if len(a) != len(b) and b.shape[0] + 1 != b.shape[1]:
    raise Exception("Incorrect format " + str(len(a) != len(b)))
n = len(a)

graph = create_differential_graph(a,b)
for i,row in enumerate(graph):
    for j,el in enumerate(row):
        if el != -1:
            print get_bool(i,n), get_bool(j,n), el
print graph
matplotlib.draw(graph)
