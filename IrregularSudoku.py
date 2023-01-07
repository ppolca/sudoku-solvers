#!/usr/bin/python3

from RegularSudoku import RegularSudoku
from SingleVar import SingleVar
import tkinter
import tkinter.messagebox
import sys

class IrregularSudoku(RegularSudoku):
    def print_board(self):
        """Print the current board in a human readable manner"""
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
        """Have user enter the squares that are in each of the 9 groups on the board"""
        box = tkinter.Tk()
        width = box.winfo_screenwidth()
        height = box.winfo_screenheight()
        box.title("Group Input")
        geo = "350x400+" + str(int(width/2 - 200)) + "+" + str(int(height/2 - 250))
        box.geometry(geo)
        instruct = tkinter.Frame(box)
        instruct.pack(side="top")
        nums = tkinter.Frame(box)
        nums.place(relx=0.5, rely=0.5, anchor="center")
        sub = tkinter.Frame(box)
        sub.pack(side="bottom")
        instructions = tkinter.Label(instruct, text="Select all squares in one group on the\nboard to solve, then click 'Confirm group.'\nRepeat this for all 9 groups.")
        instructions.pack()
        cnter = SingleVar()
        cnter.set_var(1)
        def button_click(button):
            if button['relief'] == 'raised':
                if len([entries[i][j] for i in range(9) for j in range(9) if entries[i][j]['text'] == cnter.get_var()]) < 9:
                    button['relief'] = 'sunken'
                    button['text'] = cnter.get_var()
                else:
                    tkinter.messagebox.showwarning(title="Error", message="9 squares already selected")
            else:
                button['relief'] = 'raised'
                button['text'] = 'X'
        entries = [[None for j in range(9)] for i in range(9)]
        for i in range(9):
            for j in range(9):
                entries[i][j] = tkinter.Button(nums, text="X", command=(lambda x=i,y=j: button_click(entries[x][y])))
                entries[i][j].grid(row=10*(i+1), column=10*(j+1))
        def get_group():
            vals = []
            curr_btns = [(i,j) for i in range(9) for j in range(9) if entries[i][j]['text'] == cnter.get_var()]
            if len(curr_btns) == 9:
                vals = curr_btns
                for xy in curr_btns:
                    entries[xy[0]][xy[1]]['state'] = 'disabled'
                cnter.set_var(cnter.get_var()+1)
                if cnter.get_var() == 10:
                    box.destroy()
            else:
                tkinter.messagebox.showwarning(title="Error", message="Not enough squares selected")
            return vals
        groups = []
        submit = tkinter.Button(sub, text="Confirm group", command=(lambda: groups.append(get_group())))
        submit.pack()
        box.mainloop()
        ret = list(filter(None, groups))
        if len(ret) == 9:
            self.groups = ret
        else:
            sys.exit()