import numpy as np


class ClockSubstitution:
    def __init__(self, block_number, block_size, additional_blocks=0, probabilistic=False):
        total_block_number = block_number + additional_blocks
        start_matrix = np.identity(total_block_number * block_size)
        blocks = []
        for i in range(total_block_number):
            blocks.append(start_matrix[:, i * block_size: (i + 1) * block_size])
        self.blocks = blocks
        self.block_size = block_size
        self.block_number = block_number
        self.total_block_number = total_block_number
        self.xor_matrix = self.create_xor_matrix(block_size, probabilistic)
        self.plus_matrix = self.create_plus_matrix(block_size, probabilistic)
        self.substitution_matrix = self.create_substitution_matrix(block_size, probabilistic)

    @staticmethod
    def create_xor_matrix(block_size, probabilistic):
        identity = np.identity(block_size)
        result = np.zeros((2 * block_size, 2 * block_size))
        result[:block_size, :block_size] = identity.copy()
        result[block_size:block_size * 2, :block_size] = identity.copy()
        result[block_size:block_size * 2, block_size:block_size * 2] = identity.copy()
        return result

    @staticmethod
    def __create_um__(block_size, probabilistic):
        um = np.zeros((block_size, block_size))
        if probabilistic:
            for i in range(block_size):
                for j in range(i, block_size):
                    um[i][j] = 2 ** (i - j)
        else:
            for i in range(block_size):
                for j in range(i, block_size):
                    um[i][j] = 1
        return um

    @staticmethod
    def create_plus_matrix(block_size, probabilistic):
        um = ClockSubstitution.__create_um__(block_size, probabilistic)
        result = np.zeros((block_size * 2, block_size * 2))
        result[:block_size, :block_size] = um.copy()
        result[block_size:2 * block_size, :block_size] = um.copy()
        result[block_size:2 * block_size, block_size:2 * block_size] = np.identity(block_size)
        return result

    @staticmethod
    def create_substitution_matrix(block_size, probabilistic):
        result = np.ones((block_size, block_size))
        if probabilistic:
            result *= 0.5
        return result

    def glue_two_blocks(self, block1, block2):
        result = np.zeros((self.block_size * self.total_block_number, self.block_size * 2))
        result[:, :self.block_size] = block1.copy()
        result[:, self.block_size:] = block2.copy()
        return result

    def __binary_operation__(self, block_num1, block_num2, operation_matrix):
        block1, block2 = self.blocks[block_num1], self.blocks[block_num2]
        concatenated = self.glue_two_blocks(block1, block2)
        operation_result = np.dot(concatenated, operation_matrix)
        self.blocks[block_num1] = operation_result[:, :self.block_size]
        self.blocks[block_num2] = operation_result[:, self.block_size:]

    def xor(self, block_num1, block_num2):
        self.__binary_operation__(block_num1, block_num2, self.xor_matrix)

    def plus(self, block_num1, block_num2):
        self.__binary_operation__(block_num1, block_num2, self.plus_matrix)

    def substitution(self, block_num):
        self.blocks[block_num] = np.dot(self.blocks[block_num], self.substitution_matrix)

    def __create_permutation_matrix__(self, permutation):
        permutation_set = set(permutation)
        for i in range(self.block_size):
            if i + 1 not in permutation_set:
                raise ValueError("Permutation should contain numbers from 1 to {}".format(self.block_size))
        result = np.zeros((self.block_size, self.block_size))
        for j, i in enumerate(permutation):
            result[i][j] = 1
        return result

    def permutation(self, block_num, permutation):
        permutation_matrix = self.__create_permutation_matrix__(permutation)
        self.blocks[block_num] = np.dot(self.blocks[block_num], permutation_matrix)

    def swap(self, block_num1, block_num2):
        self.blocks[block_num1], self.blocks[block_num2] = self.blocks[block_num2], self.blocks[block_num1]

    def __create_G_matrix__(self, shift_size):
        res = np.zeros((self.block_size, self.block_size))
        shift = np.zeros((self.block_size, self.block_size))
        quort = self.block_size / 4
        for i in range(self.block_size):
            for j in range(self.block_size):
                if i // quort == j // quort:
                    res[i][j] = 0.5
                if (i + shift_size) % self.block_size == j:
                    shift[i][j] = 1
        return np.dot(res, shift)

    def g(self, block_num, shift_size):
        return np.dot(self.blocks[block_num], self.__create_G_matrix__(shift_size))

    def dependency_matrix(self):
        return np.concatenate(self.blocks, axis=1)[:self.block_number * self.block_size,
                                                   :self.block_number * self.block_size]


def create_belt_dependency_matrix():
    belt = ClockSubstitution(4, 32, 1, True)
    belt.blocks[-1] = belt.g(0, 5)  # b = xor(b, makeG(a, 5))
    belt.xor(1, -1)
    belt.blocks[-1] = belt.g(3, 21)  # c = xor(c, makeG(d,21))
    belt.xor(2, -1)
    belt.blocks[-1] = belt.g(1, 13)  # a = plus(a, makeG(b,13))
    belt.plus(0, -1)
    belt.blocks[-1] = belt.blocks[1]  # e = makeG(plus(b,c),21)
    belt.plus(-1, 2)
    belt.blocks[-1] = belt.g(-1, 21)
    belt.plus(1, -1)  # b = plus(b,e)
    belt.plus(2, -1)  # c = plus(c,e)
    belt.blocks[-1] = belt.g(2, 13)
    belt.plus(3, -1)
    belt.blocks[-1] = belt.g(0, 21)
    belt.xor(1, -1)
    belt.blocks[-1] = belt.g(3, 5)
    belt.xor(2, -1)
    belt.swap(0, 1)
    belt.swap(2, 3)
    belt.swap(1, 2)
    belt.swap(0, 1)
    belt.swap(1, 3)
    belt.swap(2, 3)
    return belt


if __name__ == '__main__':
    belt = create_belt_dependency_matrix()
    with open("belt.txt", "w") as out:
        belt_to_write = [" ".join(map(str, row)) for row in belt.dependency_matrix()]
        out.write("\n".join(belt_to_write))
