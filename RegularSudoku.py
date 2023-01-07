#!/usr/bin/python3

from copy import deepcopy
from SingleVar import SingleVar
from SudokuState import SudokuState
import itertools
import tkinter
import sys

class RegularSudoku(SudokuState):
    def is_goal(self):
        """Return True if this is a goal/solution, False otherwise"""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0 or self.rem_v[i][j] != []:
                    return False
        return True
    
    def get_board(self):
        """Let the user input the known numbers on the given board"""
        box = tkinter.Tk()
        width = box.winfo_screenwidth()
        height = box.winfo_screenheight()
        box.title("Board Input")
        geo = "250x325+" + str(int(width/2 - 150)) + "+" + str(int(height/2 - 250))
        box.geometry(geo)
        instruct = tkinter.Frame(box)
        instruct.pack(side="top")
        nums = tkinter.Frame(box)
        nums.place(relx=0.5, rely=0.5, anchor="center")
        sub = tkinter.Frame(box)
        sub.pack(side="bottom")
        instructions = tkinter.Label(instruct, text="Please enter the numbers of the\npuzzle you wish to solve. Leave\nboxes blank if they are not filled.")
        instructions.pack()
        entries = [[None for j in range(9)] for i in range(9)]
        for i in range(9):
            for j in range(9):
                entries[i][j] = tkinter.Entry(nums, width=2)
                entries[i][j].grid(row=10*(i+1), column=10*(j+1))
        def gather_entries():
            board = [[None for j in range(9)] for i in range(9)]
            for i in range(9):
                for j in range(9):
                    try:
                        board[i][j] = int(entries[i][j].get())
                        if board[i][j] not in range(1,10):
                            board[i][j] = 0
                    except:
                        board[i][j] = 0
            box.destroy()
            return board
        board = SingleVar()
        submit = tkinter.Button(sub, text="SUBMIT", command=(lambda: board.set_var(gather_entries())))
        submit.pack()
        box.mainloop()
        self.board = board.get_var()
        if self.board is None:
            sys.exit()
    
    def print_board_standard(self):
        """Print the current board in a human readable manner as a regular board"""
        ud = self.chars["ud"]
        sep = " " + self.chars["ud"] + " "
        full_board = [ud + " " + " ".join(map(str, i[0:3])) + sep + " ".join(map(str, i[3:6])) + sep + " ".join(map(str, i[6:])) + " " + ud for i in self.board]
        def span_str(main, inter):
            return (main*7) + inter + (main*7) + inter + (main*7)
        full_board.insert(0, self.chars["rd"] + span_str(self.chars["lr"], self.chars["lrd"]) + self.chars["ld"])
        full_board.insert(4, self.chars["rud"] + span_str(self.chars["lr"], self.chars["lrud"]) + self.chars["lud"])
        full_board.insert(8, self.chars["rud"] + span_str(self.chars["lr"], self.chars["lrud"]) + self.chars["lud"])
        full_board.append(self.chars["ru"] + span_str(self.chars["lr"], self.chars["lru"]) + self.chars["lu"])
        print("\n".join(full_board))
    
    def print_board_dynamic(self):
        """Print the current board in a human readable manner based on groups"""
        full_board = []
        def same_groups(s1, s2):
            check = False
            for i in self.groups:
                if s1 in i:
                    if s2 in i:
                        check = True
                    else:
                        return False
                elif s2 in i:
                    if s1 in i:
                        check = True
                    else:
                        return False
            return check
        def which_char(left, right, up, down):
            left = "l" if left == self.chars["lr"] else ""
            right = "r" if right == self.chars["lr"] else ""
            up = "u" if up == self.chars["ud"] else ""
            down = "d" if down == self.chars["ud"] else ""
            char_to_get = left+right+up+down
            if char_to_get == "":
                return " "
            else:
                return self.chars[char_to_get]
        temp = ""
        for j in range(8):
            temp += str(self.board[0][j])
            temp += " " if same_groups((0,j), (0,j+1)) else self.chars["ud"]
        temp += str(self.board[0][j+1])
        full_board.append(temp)
        for i in range(1,9):
            temp = ""
            sepa = ""
            for j in range(8):
                temp += str(self.board[i][j])
                temp += " " if same_groups((i,j), (i,j+1)) else self.chars["ud"]
                sepa += "  " if same_groups((i-1,j), (i,j)) else self.chars["lr"]+" "
            temp += str(self.board[i][j+1])
            sepa += " " if same_groups((i-1,j+1), (i,j+1)) else self.chars["lr"]
            for l in range(1, len(sepa), 2):
                sepa = sepa[:l] + which_char(sepa[l-1], sepa[l+1], full_board[-1][l], temp[l]) + sepa[l+1:]
            full_board.append(sepa)
            full_board.append(temp)
        for i in range(len(full_board)):
            l = self.chars["rud"] if full_board[i][0] == self.chars["lr"] else self.chars["ud"]
            r = self.chars["lud"] if full_board[i][-1] == self.chars["lr"] else self.chars["ud"]
            full_board[i] = l + full_board[i] + r
        span_top = "".join([self.chars["lrd"] if i == self.chars["ud"] else self.chars["lr"] for i in full_board[0][1:-1]])
        span_bot = "".join([self.chars["lru"] if i == self.chars["ud"] else self.chars["lr"] for i in full_board[-1][1:-1]])
        full_board.insert(0, self.chars["rd"] + span_top + self.chars["ld"])
        full_board.append(self.chars["ru"] + span_bot + self.chars["lu"])
        print("\n".join(full_board))
    
    def calc_groups(self):
        """Calculate the coordinates of each square in each group"""
        self.groups = [list(itertools.product(i,j)) for i,j in itertools.product([range(3),range(3,6),range(6,9)], repeat=2)]
    
    def groups_min_me(self, x, y):
        """Return list of coordinates that includes all squares in the same group as (x,y) without (x,y) itself"""
        ret = []
        for i in self.groups:
            if (x,y) in i:
                ret += [j for j in i if j != (x,y)]
        return ret
    
    def calc_csp_graph(self):
        """Initialize CSP graph"""
        self.csp_graph = [[list(set(self.groups_min_me(i,j) + [(m,j) for m in range(9)] + [(i,m) for m in range(9)])) for j in range(9)] for i in range(9)]
    
    def calc_rem_v(self):
        """Initialize remaining values table"""
        self.rem_v = [[list(range(1, 10)) if j == 0 else [] for j in i] for i in self.board]
        for i in range(9):
            for j in range(9):
                self.update_rem_v(i, j)
    
    def update_rem_v(self, x, y):
        """Update remaining values for (x,y)"""
        for i,j in self.csp_graph[x][y]:
            try:
                self.rem_v[x][y].remove(self.board[i][j])
            except:
                pass
    
    def update_rem_v_of_related(self, x, y):
        """Update remaining values for each entry in CSP graph by removing number at (x,y)"""
        for i,j in self.csp_graph[x][y]:
            try:
                self.rem_v[i][j].remove(self.board[x][y])
            except:
                pass
    
    def set_val(self, x, y, val):
        """Set value on board and update rem_v of any affected square"""
        self.board[x][y] = val
        self.rem_v[x][y] = []
        self.update_rem_v_of_related(x, y)
    
    def solve(self):
        """Try to solve problem - if it can, return board solution, else return None"""
        if self.is_goal():
            return self.board
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0 and self.rem_v[i][j] == []:
                    return False
        mrv = 10
        xm = 0
        ym = 0
        for i in range(9):
            for j in range(9):
                if 1 <= len(self.rem_v[i][j]) < mrv:
                    mrv = len(self.rem_v[i][j])
                    xm = i
                    ym = j
        subproblems = []
        for i in self.rem_v[xm][ym]:
            sp = self.__class__(board=deepcopy(self.board), csp_graph=self.csp_graph, rem_v=deepcopy(self.rem_v), groups=self.groups)
            sp.set_val(xm, ym, i)
            rem_v_len = sum([len(sp.rem_v[i][j]) for i,j in sp.csp_graph[xm][ym]])
            subproblems.append((sp, rem_v_len))
        subproblems.sort(key=lambda x: x[1])
        while subproblems != []:
            ans = subproblems.pop()[0].solve()
            if ans != False:
                self.board = ans
                return ans
        return False