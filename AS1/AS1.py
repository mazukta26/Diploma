import numpy as np
import collections


class AS1:
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
        return AS1(a, b)

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
            trans.append(AS1.diff_oper(row * v))
        res = AS1.get_transitions_by_tuples(trans)
        return res, s

    def create_differential_graph(self):
        graph = np.full((2 ** self.n, 2 ** self.n), fill_value=-1, dtype='int64')
        for i in range(2 ** self.n):
            v = self._get_bool(i)
            all_transitions, their_s = self.get_transitions_by_abv(v)
            for trans in all_transitions:
                graph[i, AS1._get_int(trans)] = their_s
        return graph

    def get_alphas(self, beta):
        s = beta * self.b[:, -1]
        alphas = []
        for a, b in zip(self.a, self.b.T):
            alphas.append((beta * b).tolist())
            if a:
                alphas[-1].extend(s)
        alpha_tuples = [AS1.diff_oper(alpha) for alpha in alphas]
        return AS1.get_transitions_by_tuples(alpha_tuples)

    def create_linear_transitions_graph(self):
        graph = np.full((2 ** self.n, 2 ** self.n), fill_value=-1, dtype='int64')
        alpha_beta_dict = collections.defaultdict(list)
        for beta_num in range(2 ** self.n):
            beta = np.array(self._get_bool(beta_num))
            for alpha in self.get_alphas(beta):
                alpha_beta_dict[tuple(alpha)].append(beta)
        for alpha in alpha_beta_dict:
            s = int(np.sum(np.array(alpha) * self.a) > 0)
            for beta in alpha_beta_dict[alpha]:
                graph[AS1._get_int(alpha), AS1._get_int(beta)] = s
        return graph

    @staticmethod
    def write_graph_into_file(graph, filename):
        with open(filename, 'w') as f:
            for row in graph:
                f.write(",".join(str(el) for el in row) + "\n")

if __name__ == '__main__':
    skipjacka = AS1.read_from_file('skipjacka.txt', ' ')
    diff_graph = skipjacka.create_differential_graph()
    lin_graph = skipjacka.create_linear_transitions_graph()
    AS1.write_graph_into_file(diff_graph, 'skipjacka_diff.txt')
    AS1.write_graph_into_file(lin_graph, 'skipjacka_lin.txt')