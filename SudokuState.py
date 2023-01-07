#!/usr/bin/python3

#TODO:
# image recognition for game initialization
# print outside borders

class SudokuState():
    def __init__(self, board=None, csp_graph=None, rem_v=None, groups=None):
        """Initialize variables"""
        self.board = board
        self.csp_graph = csp_graph
        self.rem_v = rem_v
        self.groups = groups
        self.chars = {"lr":"\u2500", "ud":"\u2502", "ru":"\u2514", "lu":"\u2518", "ld":"\u2510", "rd":"\u250c", "rud":"\u251c", "lud":"\u2524",
                    "lru":"\u2534", "lrd":"\u252c", "lrud":"\u253c"}
    
    def setup(self):
        """Initialize problem"""
        self.get_board()
        self.calc_groups()
        self.calc_csp_graph()
        self.calc_rem_v()
    
    def get_board(self):
        pass

    def calc_groups(self):
        pass

    def calc_csp_graph(self):
        pass

    def calc_rem_v(self):
        pass