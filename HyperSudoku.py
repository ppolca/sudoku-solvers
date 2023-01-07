#!/usr/bin/python3

from RegularSudoku import RegularSudoku
import itertools

class HyperSudoku(RegularSudoku):
    def calc_groups(self):
        super().calc_groups()
        self.groups += [list(itertools.product(i,j)) for i,j in itertools.product([range(1,4), range(5,8)], repeat=2)]