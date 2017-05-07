import sys
import numpy as np
import collections


class XS1:
    def __init__(self, a, b):
        n = len(a)
        self.a, self.b, self.n = np.array(a), np.array(b), n

    @staticmethod
    def read_from_file(input_filename, sep):
        with open(input_filename, 'r') as inp:
            lines = inp.readlines()
            lines = [line.strip() for line in lines if line.strip()]
            matrix = np.array([list(map(int, line.split(sep))) for line in lines])
        if matrix.shape[0] != matrix.shape[1]:
            raise IOError("Incorrect format of a and B")
        a = matrix[:-1, -1].flatten()
        b = matrix[:, :-1].T
        return XS1(a, b)

    @staticmethod
    def _get_int(bool_arr):
        res = 0
        for bit in bool_arr:
            res *= 2
            res += bit
        return res

    def _get_bool(self, num):
        res = []
        while num > 0:
            res.append(num % 2)
            num //= 2
        res += [0] * (self.n - len(res))
        return res[::-1]

    @staticmethod
    def diff_oper(operands):
        if np.sum(operands) == 0:
            return 0,
        if np.sum(operands) == 1:
            return 1,
        return 0, 1

    @staticmethod
    def get_transitions_by_tuples(tuples):
        res = []
        for bit in tuples[0]:
            res.append([bit])
        for tup in tuples[1:]:
            l = len(res)
            if len(tup) == 2:
                res += [el[:] for el in res]
            for i, bit in enumerate(tup):
                for j in range(l):
                    res[i * l + j].append(bit)
        return res

    def get_transitions_by_abv(self, v):
        s = int(np.sum(self.a * v > 0) > 0)
        v.append(s)
        trans = []
        for row in self.b:
            trans.append(XS1.diff_oper(row * v))
        res = XS1.get_transitions_by_tuples(trans)
        return res, s

    def create_differential_graph(self):
        graph = np.full((2 ** self.n, 2 ** self.n), fill_value=-1, dtype='int64')
        for i in range(2 ** self.n):
            v = self._get_bool(i)
            all_transitions, their_s = self.get_transitions_by_abv(v)
            for trans in all_transitions:
                graph[i, XS1._get_int(trans)] = their_s
        return graph

    def get_alphas(self, beta):
        weights = XS1.diff_oper(beta * self.b[:, -1])
        result_by_weight = dict()
        for weight in weights:
            alphas = []
            for a, b in zip(self.a, self.b.T):
                alphas.append((beta * b).tolist())
                alphas[-1].append(weight*a)
            alpha_tuples = [XS1.diff_oper(alpha) for alpha in alphas]
            result_by_weight[weight] = XS1.get_transitions_by_tuples(alpha_tuples)
        return result_by_weight

    @staticmethod
    def weight_selecting_multiedge(was, now):
        if was == -1:
            return now
        return min(was, now)

    def create_linear_transitions_graph(self):
        graph = np.full((2 ** self.n, 2 ** self.n), fill_value=-1, dtype='int64')
        for beta_num in range(2 ** self.n):
            beta = np.array(self._get_bool(beta_num))
            alphas_by_weights = self.get_alphas(beta)
            for weight, alphas in alphas_by_weights.items():
                for alpha in alphas:
                    graph[XS1._get_int(alpha), XS1._get_int(beta)] =\
                        XS1.weight_selecting_multiedge(graph[XS1._get_int(alpha), XS1._get_int(beta)], weight)
        return graph

    @staticmethod
    def write_graph_into_file(graph, filename):
        with open(filename, 'w') as f:
            for row in graph:
                f.write(",".join(str(el) for el in row) + "\n")

if __name__ == '__main__':
    scheme_filename, scheme_name = sys.argv[1:]
    scheme = XS1.read_from_file(scheme_filename, ' ')
    diff_graph = scheme.create_differential_graph()
    lin_graph = scheme.create_linear_transitions_graph()
    XS1.write_graph_into_file(diff_graph, '{}_diff.txt'.format(scheme_name))
    XS1.write_graph_into_file(lin_graph, '{}_lin.txt'.format(scheme_name))