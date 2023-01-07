#!/usr/bin/python3

from RegularSudoku import RegularSudoku
import itertools

class OffsetSudoku(RegularSudoku):
    def calc_groups(self):
        super().calc_groups()
        self.groups += [[(m,n) for m,n in itertools.product([i, i+3, i+6], [j, j+3, j+6])] for i,j in itertools.product(range(3), repeat=2)]