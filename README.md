# CSP-BACKTRACKING-SEARCH-sudokusolver
1. The creative parts for this CSP backtracking search algorithm:\
         In this efficient algorithm, it covers the minimum-remaining-values (MRV) heuristic for value assignment, arc-consistent rule for constraint checking, forword checking algorithm to efficiently prune out values that violate constraints in the future, and backtracking search algorithm.

2. Represent sudoku problem as CSP (constraint satisfaction problems), the three properties of the CSP are defined as follow:

         Variables: Each cell (row, column) on the sudoku puzzle.
         Domains: For each empty cell, a domain is defined as a set of numbers between 1 and 9.
                  For each pre-filled cell, a domain is the existed value.  
         Constraints: No redundant numbers in rows, columns and the 3 x 3 regions that the cell is in.

3. The algorithm is BACKTRACKING-SEARCH from chapter 6 Constraint Satisfaction Problem of the book: Artificial Intelligence A mdoern Approach (4th edit).

         The minimum-remaining-values (MRV) heuristic is used to select the next variable to assgin value.
         Arc-consistent is used to check constraint satisfaction.
         Forward checking algorithm to avoid an assignment that would cause failure in the future, meanwhile we prune out values in cell_domain that violate constraints in the future.
