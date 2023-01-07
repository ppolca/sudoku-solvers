#!/usr/bin/python3

from SudokuState import SudokuState
from RegularSudoku import RegularSudoku as Reg
from IrregularSudoku import IrregularSudoku as Irr
from SudokuX import SudokuX as X
from OffsetSudoku import OffsetSudoku as Off
from HyperSudoku import HyperSudoku as Hyp

ss = Hyp()
ss.setup()
if (ans := ss.solve()) == False:
    print("Unsolvable")
else:
    ss.print_board_standard()
    ss.print_board_dynamic()