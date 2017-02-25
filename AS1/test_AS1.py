import AS1
import numpy as np
from unittest import TestCase


class TestAS1(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.successful_input = 'successful_input'
        cls.failing_input = 'failing_input'
        with open(cls.failing_input, 'w') as inp:
            zeros = "0,0,0\n"
            inp.write(zeros*4)
        a = [1, 0, 1]
        b = [[1, 1, 0, 1], [0, 1, 1, 0], [1, 0, 1, 0]]
        pseudo_a = a[:] + [0]
        pseudo_b = b[:]
        pseudo_b.append(pseudo_a)
        pseudo_b = np.array(pseudo_b).T
        with open(cls.successful_input, 'w') as inp:
            inp.write("\n".join([",".join(map(str, line)) for line in pseudo_b]))
        cls.a, cls.b = a, b

    def test_read_from_file_failure(self):
        caught = False
        try:
            _ = AS1.AS1.read_from_file(self.failing_input, ',')
        except IOError:
            caught = True
        else:
            pass
        if not caught:
            self.fail('Expected IOError')

    def test_read_from_file_success(self):
        successful = AS1.AS1.read_from_file(self.successful_input, ',')
        assert np.all(self.a == successful.a) and np.all(np.array(self.b) == successful.b),\
            'Input for a and B is not equal to output'

    def test_get_int(self):
        assert AS1.AS1._get_int([1, 0, 0, 1, 0, 1, 1]) == 75
        assert AS1.AS1._get_int([0, 0, 0, 0, 0]) == 0

    def test_get_bool(self):
        obj = AS1.AS1.read_from_file(self.successful_input, ',')
        assert obj._get_bool(3) == [0, 1, 1]
        assert obj._get_bool(7) == [1, 1, 1]
        assert obj._get_bool(0) == [0, 0, 0]

    def test_diff_oper(self):
        assert AS1.AS1.diff_oper([0, 0, 0, 0, 0]) == (0,)
        assert AS1.AS1.diff_oper([0, 1, 0, 0, 0, 0]) == (1,)
        assert AS1.AS1.diff_oper([0, 1, 0, 1, 0, 0, 0]) == (0, 1) or AS1.AS1.diff_oper([0, 1, 0, 1, 0, 0, 0]) == (1, 0)
        assert AS1.AS1.diff_oper([1, 1, 1, 1]) == (0, 1) or AS1.AS1.diff_oper([1, 1, 1, 1]) == (1, 0)
        assert AS1.AS1.diff_oper([1]) == (1,)
        assert AS1.AS1.diff_oper([0]) == (0,)

    def test_get_transitions_by_tuples(self):
        tuples = [(1,), (0,), (0, 1), (1,), (0, 1)]
        should_have = [[1, 0, 0, 1, 0],
                       [1, 0, 1, 1, 0],
                       [1, 0, 0, 1, 1],
                       [1, 0, 1, 1, 1]]
        result = AS1.AS1.get_transitions_by_tuples(tuples)
        assert len(result) == np.prod(list(map(len, tuples)))
        assert all([len(res) == len(tuples) for res in result])
        assert all([should_have_example in result for should_have_example in should_have])

    def test_get_transitions_by_abv(self):
        obj = AS1.AS1.read_from_file(self.successful_input, ',')
        v = [1, 0, 0]
        expected = [[0, 0, 1], [1, 0, 1]]
        gotten_trans, gotten_s = obj.get_transitions_by_abv(v)
        assert gotten_s == 1
        assert len(gotten_trans) == len(expected) and all([exp_example in gotten_trans for exp_example in expected])
        gotten_trans, gotten_s = obj.get_transitions_by_abv([0, 1, 0])
        assert gotten_s == 0
        assert gotten_trans == [[1, 1, 0]]

    def test_create_differential_graph(self):
        obj = AS1.AS1.read_from_file(self.successful_input, ',')
        expected = np.array([[0, -1, -1, -1, -1, -1, -1, -1],
                             [-1, -1, -1, -1, -1, -1, -1,  1],
                             [-1, -1, -1, -1, -1, -1,  0, -1],
                             [-1,  1, -1, 1, -1, 1, -1, 1],
                             [-1, 1, -1, -1, -1, 1, -1, -1],
                             [-1, -1, 1, 1, -1, -1, 1, 1],
                             [-1, -1, -1, 1, -1, -1, -1, 1],
                             [1, 1, 1, 1, 1, 1, 1, 1]])
        gotten = np.array(obj.create_differential_graph())
        assert np.all(gotten == expected)

    def test_get_alphas(self):
        obj = AS1.AS1.read_from_file(self.successful_input, ',')
        expected = [[0, 1, 1], [1, 1, 1], [0, 1, 0], [1, 1, 0]]
        gotten = obj.get_alphas([1, 0, 1])
        assert len(gotten) == len(expected) and all([expected_example in gotten for expected_example in expected])

    def test_create_linear_transitions_graph(self):
        obj = AS1.AS1.read_from_file(self.successful_input, ',')
        expected = np.array([[0, -1, -1, -1, -1, -1, 0, 0],
                             [-1, -1, -1, -1, -1, -1, 1, 1],
                             [-1, -1, -1, -1, -1, 0, 0, 0],
                             [-1, -1, 1, -1, 1, 1, 1, 1],
                             [-1, -1, -1, -1, -1, -1, 1, 1],
                             [-1, 1, -1, -1, -1, -1, 1, 1],
                             [-1, -1, -1, 1, -1, 1, 1, 1],
                             [-1, -1, -1, 1, 1, 1, 1, 1]])
        gotten = obj.create_linear_transitions_graph()
        assert np.all(gotten == expected)

    def test_write_graph_into_file(self):
        obj = AS1.AS1.read_from_file(self.successful_input, ',')
        expected = np.array([[0, -1, -1, -1, -1, -1, 0, 0],
                             [-1, -1, -1, -1, -1, -1, 1, 1],
                             [-1, -1, -1, -1, -1, 0, 0, 0],
                             [-1, -1, 1, -1, 1, 1, 1, 1],
                             [-1, -1, -1, -1, -1, -1, 1, 1],
                             [-1, 1, -1, -1, -1, -1, 1, 1],
                             [-1, -1, -1, 1, -1, 1, 1, 1],
                             [-1, -1, -1, 1, 1, 1, 1, 1]])
        obj.write_graph_into_file(obj.create_linear_transitions_graph(), "linear_trans")
        file_lines = open('linear_trans', 'r').readlines()
        gotten = np.array([list(map(lambda x: int(x.strip()), line.split(","))) for line in file_lines])
        assert np.all(gotten == expected)







