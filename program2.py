# Programming Assignment 2 - Jan Ahmed

import math
import copy
from typing import List
from sudoku_constraints9x9 import constraint9x9

# Sudoku class
class Sudoku:
    def __init__(self, board=None):
        self.variables = {}
        self.constraints = {}
        self.n = 0
        if board is not None:
            self.init_vars(board)
            self.n = len(board)
        self.adjacency = {}

    # Setting the variables
    def init_vars(self, board):
        for i in range(1,len(board)+1):
            for j in range(1,len(board)+1):
                if board[i-1][j-1] != None:
                    self.variables[f'C{i}{j}'] = [board[i-1][j-1]]
                else:
                    self.variables[f'C{i}{j}'] = [x for x in range(1,len(board)+1)]

    def __deepcopy__(self, memo):
        new_sudoku = Sudoku()
        new_sudoku.variables = copy.deepcopy(self.variables, memo)
        new_sudoku.constraints = self.constraints
        new_sudoku.n = self.n
        new_sudoku.adjacency = self.adjacency

        return new_sudoku

    def init_adjacency(self):
        for arc in list(self.constraints.keys()):
            if arc[0] in self.adjacency:
                self.adjacency[arc[0]].append(arc[1])
            else:
                self.adjacency[arc[0]] = [arc[1]]
            
            if arc[1] in self.adjacency:
                self.adjacency[arc[1]].append(arc[0])
            else:
                self.adjacency[arc[1]] = [arc[0]] 

    # Setting the constraints (for general board size)
    def init_constraints(self):
        n = self.n
        for row in range(1,n+1):
            for i in range(1,n+1):
                for j in range(i+1,n+1):
                    key = (f'C{row}{i}', f'C{row}{j}')
                    self.constraints[key] = [[x,y] for x in range(1,n+1) for y in range(1,n+1) if x!=y]

        for column in range(1,n+1):
            for i in range(1,n+1):
                for j in range(i+1, n+1):
                    key = (f'C{i}{column}', f'C{j}{column}')
                    self.constraints[key] = [[x,y] for x in range(1,n+1) for y in range(1,n+1) if x!=y]

        k = int(math.sqrt(n))
        for box in range(n):
            for i in range(n):
                for j in range(i+1,n):
                    key = (f'C{i//k+(box//k)*k+1}{i%k+(box%k)*k+1}', f'C{j//k+(box//k)*k+1}{j%k+(box%k)*k+1}')
                    if key not in self.constraints and ((key[1],key[0]) not in self.constraints):
                        self.constraints[key] = [[x,y] for x in range(1,n+1) for y in range(1,n+1) if x!=y]
    
    def print_sudoku(self):
        print("# Variables:")        
        print(self.variables)
        print()
        print("# Constraints:")
        print(self.constraints)
        print()

# Example puzzles

puzzle_1 = [
    [7, None, None, 4, None, None, None, 8, 6],
    [None, 5, 1, None, 8, None, 4, None, None],
    [None, 4, None, 3, None, 7, None, 9, None],
    [3, None, 9, None, None, 6, 1, None, None],
    [None, None, None, None, 2, None, None, None, None],
    [None, None, 4, 9, None, None, 7, None, 8],
    [None, 8, None, 1, None, 2, None, 6, None],
    [None, None, 6, None, 5, None, 9, 1, None],
    [2, 1, None, None, None, 3, None, None, 5]
]

puzzle_2 = [
    [1, None, None, 2, None, 3, 8, None, None],
    [None, 8, 2, None, 6, None, 1, None, None],
    [7, None, None, None, None, 1, 6, 4, None],
    [3, None, None, None, 9, 5, None, 2, None],
    [None, 7, None, None, None, None, None, 1, None],
    [None, 9, None, 3, 1, None, None, None, 6],
    [None, 5, 3, 6, None, None, None, None, 1],
    [None, None, 7, None, 2, None, 3, 9, None],
    [None, None, 4, 1, None, 9, None, None, 5]
]

puzzle_3 = [
    [1, None, None, 8, 4, None, None, 5, None],
    [5, None, None, 9, None, None, 8, None, 3],
    [7, None, None, None, 6, None, 1, None, None],
    [None, 1, None, 5, None, 2, None, 3, None],
    [None, 7, 5, None, None, None, 2, 6, None],
    [None, 3, None, 6, None, 9, None, 4, None],
    [None, None, 7, None, 5, None, None, None, 6],
    [4, None, 1, None, None, 6, None, None, 7],
    [None, 6, None, None, 9, 4, None, None, 2]
]

# Part 2:

def revise(sudoku_csp: Sudoku, var1: str, var2: str) -> bool:
    removed = False
    constraint = (sudoku_csp.constraints[(var1, var2)] if (var1, var2) in sudoku_csp.constraints 
              else sudoku_csp.constraints[(var2, var1)] if (var2, var1) in sudoku_csp.constraints 
              else None)
    if constraint == None:
        return False

    for i,x in enumerate(sudoku_csp.variables[var1]):
        found = False
        for y in sudoku_csp.variables[var2]:
            if [x,y] in constraint:
                found = True
                break
        if not found:
            del sudoku_csp.variables[var1][i]
            removed = True
    
    return removed

# End of Part 2

# Part 3:

def AC3(sudoku_csp: Sudoku, queue) -> bool:
    while len(queue) > 0:
        arc = queue.pop(0)
        if revise(sudoku_csp, arc[0], arc[1]):
            if len(sudoku_csp.variables[arc[0]]) == 0:
                return False
            for neighbor in sudoku_csp.adjacency[arc[0]]:
                if neighbor == arc[1]:
                    continue
                queue.append((neighbor, arc[0]))
    
    return True

# End of Part 3

# Part 4:

def minimum_remaining_values(sudoku_csp: Sudoku) -> str:
    minVal = 1000000000
    minVar = ''
    for x, domain in sudoku_csp.variables.items():
        if 1 < len(domain) < minVal:
            minVal = len(domain)
            minVar = x
    return minVar

# End of Part 4

# Part 5:

def backtrack_search(sudoku_csp: Sudoku):
    queue = list(sudoku_csp.constraints.keys())
    count = 0
    for dom in sudoku_csp.variables.values():
        if len(dom) == 1:
            count += 1 

    # Check if solvable
    if not AC3(sudoku_csp, queue):
        return False
    res = backtrack(sudoku_csp, [])
    if res:
        return res[count:]

def backtrack(sudoku_csp: Sudoku, assignment: List[int]):
    # Check what AC-3 solved
    for solved, dom in sudoku_csp.variables.items():
        if len(dom) == 1:
            if (solved, dom[0]) not in assignment:
                assignment.append((solved, dom[0]))

    var = minimum_remaining_values(sudoku_csp)
    if var == '':
        return assignment
    domain = sudoku_csp.variables[var]
    for val in domain:
        assignment.append((var, val))
        new_csp = copy.deepcopy(sudoku_csp)
        new_csp.variables[var] = [val]
        queue = [(x,var) for x in sudoku_csp.adjacency[var]]
        consistent = AC3(new_csp,queue)
        if consistent:
            result = backtrack(new_csp, assignment)
            if result:
                return result
        assignment.pop()
    return False

if __name__ == "__main__":
    # Part 1:
    mini_sudoku = [[1, None, None, None], [None, 2, None, None], [None, None, 3, None], [None, None, None, 4]]
    mini_sudoku_csp = Sudoku(mini_sudoku)

    # Setting the constraints
    mini_sudoku_csp.init_constraints()

    print("-------------- Part 1 --------------")
    mini_sudoku_csp.print_sudoku()

    # End of Part 1

    # Test backtrack
    print("-------------- Testing backtrack --------------")
    sudoku_1 = Sudoku(puzzle_1)
    sudoku_2 = Sudoku(puzzle_2)
    sudoku_3 = Sudoku(puzzle_3)
    sudoku_1.constraints = copy.deepcopy(constraint9x9)
    sudoku_2.constraints = copy.deepcopy(constraint9x9)
    sudoku_3.constraints = copy.deepcopy(constraint9x9)

    mini_sudoku_csp.init_adjacency()
    sudoku_1.init_adjacency()
    sudoku_2.init_adjacency()
    sudoku_3.init_adjacency()

    print(backtrack_search(mini_sudoku_csp))
    print(backtrack_search(sudoku_1))
    print(backtrack_search(sudoku_2))
    print(backtrack_search(sudoku_3))