#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 10:01:44 2022

@author: yuanyuan
"""
# CSP for 9x9 Sudoku puzzle:
# a set of variables: all 9x9 cells. a cell is (row, column)
# a set of domains: 1 to 9 for all empty cells, the assigned value for the prefilled cell.
# a set of constraints: each value in the same row is different.
#                       each value in the same column is different.
#                       each value in the same 3x3 region is different.

import numpy as np
from copy import deepcopy


class CSP_Sudoku:
    # represent our sudoku problem as CSP
    # each cell in the sudoku puzzle is a variable
    # each cell has its domain
    # each cell has its 20 arc neighbors that should satisfy all-different constraint


    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.size = self.sudoku[0].size # sudoku puzzle row, column size (9)
        self.solved_sudoku = np.zeros((self.size,self.size)) # store solved puzzle
        self.filled_cell = [] # a list of 'row_col' combinations, start from '00'. e.g., '12' means row 1 col 2

        self.cell_domain = np.zeros((self.size,self.size),dtype='object') # initialize a 9x9 2D array to store domain for each cell
        self.initialize_cell() # initialize cell domain for the given sudoku

        self.neighbors = {} # {key (cell name) : value (cell neighbors)}
        self.arc_neighbors() # create 20 arc neighbors for each cell, total is 81x20


    def initialize_cell(self):
        # update domain according to our given specific sudoku
        for r in range(self.size):
            for c in range(self.size):
                # for the given sudoku, empty cell is denoted by number 0
                if self.sudoku[r][c] != 0:
                    self.cell_domain[r][c] = str(self.sudoku[r][c]) # pre-filled cell, directly use the value
                else:
                    self.cell_domain[r][c] = "123456789" # empty cell, fill with default domain ('123456789')


    def arc_neighbors(self):
        # create binary neighbors for each cell, each cell has 20 "neighbor" cells,
        # they are 8 cells in its same row, 8 cells in its same column, and extra 4 cells in
        # its same region. therefore, the total size for arc_neighbors is 81x20
        for r in range(self.size):
            for c in range(self.size):
                self.neighbors[str(r)+str(c)] = list(set([str(r)+str(j) for j in range(self.size)] + # same row
                                                         [str(i)+str(c) for i in range(self.size)] + # same column
                                                         [str(i)+str(j) for i in range(r//3*3, r//3*3 + 3) for j in range(c//3*3, c//3*3 + 3)]) - # same 3x3 region
                                                         set([str(r)+str(c)])) # no duplicate for set


    def is_complete(self):
        # check if the assignment is complete, that means 81 cells have all been filled
        return len(set(self.filled_cell)) == self.size * self.size


    def select_unassigned_variables(self):
        # implement minimum-remaining-values (MRV) heuristic to select the next variable (cell)
        # for assignment
        mrv_cell = () # initialize minimum-remaining-values cell

        for r in range(self.size):
            for c in range(self.size):
                if (str(r)+str(c)) not in self.filled_cell:
                    if len(mrv_cell) == 0:
                        mrv_cell = (r,c)
                    elif (len(self.cell_domain[r][c]) < len(self.cell_domain[mrv_cell[0]][mrv_cell[1]])):
                        mrv_cell = (r,c)

        return mrv_cell


    def is_arc_consistent(self, row, col, value):
        # check the current assigned value is different with
        # other assigned values in its row, its column, and its 3x3 region
        not_in_row = value not in self.solved_sudoku[row]
        not_in_col = value not in [self.solved_sudoku[r][col] for r in range(self.size)]
        not_in_region = value not in [self.solved_sudoku[r][c] for r in range(row//3*3, row//3*3 + 3) for c in range(col//3*3, col//3*3 + 3)]

        return not_in_row and not_in_col and not_in_region


    def forward_checking(self, r, c, value):
        # do forward checking through inference to avoid an assignment that would
        # cause failure in the future. meanwhile we prune out values in cell_domain that violate constraints
        for neighbor in self.neighbors[str(r)+str(c)]:
            i = int(neighbor[0])
            j = int(neighbor[1])
            if (neighbor not in self.filled_cell) and (str(value) in self.cell_domain[i][j]):
                # if this value is the only one left in its neighbor's domain, forward checking fail
                if len(self.cell_domain[i][j])==1:
                    return False
                # otherwise update domain
                self.cell_domain[i][j] = self.cell_domain[i][j].replace(str(value), "")
                # after domain update, if neighbor's domain left with only one value, we keep constraints propagation
                if len(self.cell_domain[i][j])==1:
                    # recursively check for neighbor's neighbor cells
                    if not self.forward_checking(i, j, int(self.cell_domain[i][j])):
                        return False

        return True


    def csp_backtracking(self):
        # recursively do actions: select cell (variable), select value, check consistency,
        # assign cell with value, forward checking and update cell_domian
        if self.is_complete():
            return True

        # choose the cell with the least number of values in its domain
        mrv_cell = self.select_unassigned_variables()
        # keep a record of domain before we update it
        pre_domain = deepcopy(self.cell_domain)

        r = mrv_cell[0]
        c = mrv_cell[1]
        for value in self.cell_domain[r][c]:
            value = int(value)
            # check if the value is different with other assigned values in the same row, column and region.
            if self.is_arc_consistent(r, c, value):
                # assign value for each unassigned cell in the sudoku
                self.solved_sudoku[r][c]= value
                # after assigned a value to a cell, we put this cell in the list of filled_cells
                self.filled_cell.append(str(r)+str(c))
                # do forward checking, and update cell_domain
                if self.forward_checking(r, c, value):
                    # if the current assignemnt satisfies forward checking, move to the next cell
                    result = self.csp_backtracking()
                    if result:
                        return result

                # backtrack the last assignment if it does not satisfy forward checking
                self.solved_sudoku[r][c]= 0
                self.filled_cell.pop()
                # recover to previous cell_domain
                self.cell_domain = pre_domain

        return False



def main():

    # specific sudoku puzzles in our homework
    sudoku1 = np.array([[6,0,8,7,0,2,1,0,0],
                        [4,0,0,0,1,0,0,0,2],
                        [0,2,5,4,0,0,0,0,0],
                        [7,0,1,0,8,0,4,0,5],
                        [0,8,0,0,0,0,0,7,0],
                        [5,0,9,0,6,0,3,0,1],
                        [0,0,0,0,0,6,7,5,0],
                        [2,0,0,0,9,0,0,0,8],
                        [0,0,6,8,0,5,2,0,3]])

    sudoku2 = np.array([[0,7,0,0,4,2,0,0,0],
                        [0,0,0,0,0,8,6,1,0],
                        [3,9,0,0,0,0,0,0,7],
                        [0,0,0,0,0,4,0,0,9],
                        [0,0,3,0,0,0,7,0,0],
                        [5,0,0,1,0,0,0,0,0],
                        [8,0,0,0,0,0,0,7,6],
                        [0,5,4,8,0,0,0,0,0],
                        [0,0,0,6,1,0,0,5,0]])

    # create 2 objects for sudoku1 and sudoku2
    csp_sudoku1 = CSP_Sudoku(sudoku1)
    csp_sudoku2 = CSP_Sudoku(sudoku2)

    if csp_sudoku1.csp_backtracking() and csp_sudoku2.csp_backtracking():
        print("This is solved sudoku1: \n", csp_sudoku1.solved_sudoku, "\n")
        print("This is solved sudoku2: \n", csp_sudoku2.solved_sudoku)       
    elif not csp_sudoku1.csp_backtracking():
        print("Failing to solve the sudoku1.")
    elif not csp_sudoku2.csp_backtracking():
        print("Failing to solve the sudoku2.")
    


if __name__ == "__main__":
    main()








