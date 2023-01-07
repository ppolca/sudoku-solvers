#!/usr/bin/python3

from RegularSudoku import RegularSudoku

class SudokuX(RegularSudoku):
    def calc_groups(self):
        super().calc_groups()
        self.groups.append([(i,i) for i in range(9)])
        self.groups.append([(i,j) for i,j in zip(range(9), range(8, -1, -1))])