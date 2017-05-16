import sys
import numpy as np
from numpy import linalg as ling

with open(sys.argv[1]) as inp:
    lines = list(filter(lambda x: len(x) > 0, inp.read().split("\n")))
    lines = [list(map(float, filter(lambda x: len(x) > 0, line.split(" ")))) for line in lines]
dependency_matrix = np.array(lines)

eigenvalues = ling.eigvals(dependency_matrix)
eigenvalues = np.abs(eigenvalues)
eigenvalues = np.sort(eigenvalues)[::-1]


print("k: {}; lambda (first eigenvalue): {}".format(eigenvalues[1]/eigenvalues[0], eigenvalues[0]))

matrix_in_power = dependency_matrix.copy()
iter_max, power = dependency_matrix.shape[0], 1
while not np.all(matrix_in_power != 0) and power < iter_max:
    matrix_in_power = np.dot(matrix_in_power,dependency_matrix)
    power += 1
if power == iter_max:
    print("There is no exponent")
else:
    print("Exponent: ",power)

