# CSP-BACKTRACKING-SEARCH-sudokusolver

Represent sudoku problem as CSP (constraint satisfaction problems), the three properties of the CSP are defined as follow:

Variables: Each cell (row, column) on the sudoku puzzle.
Domains: For each empty cell, a domain is defined as a set of numbers between 1 and 9.
         For each pre-filled cell, a domain is the existed value.  
Constraints: No redundant numbers in rows, columns and the 3 x 3 regions that the cell is in.

the algorithm is BACKTRACKING-SEARCH from chapter 6 Constraint Satisfaction Problem of the book: Artificial Intelligence A mdoern Approach (4th edit).

