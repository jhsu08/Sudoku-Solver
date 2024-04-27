#!/usr/bin/env python
#coding:utf-8
import sys
import time

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)

def get_empty_cells(board):
    """Given a board, this function returns a list of empty cells (i, j) where i is the row and j is the column"""
    empty_cells = []
    for i in ROW:
        for j in COL:
            if board[i + j] == 0:
                empty_cells.append((i,j))
    return empty_cells

def mrv_heuristic(board):
    """Finds the cell with the smallest domain"""
    # get all empty cells in the Sudoku board
    empty_cells = get_empty_cells(board)
    
    # calculate the number of remaining possible values for each empty cell
    def domain_size(cell):
        row, col = cell
        return len(get_possible_values(board, row, col))
    
    # find the cell with the minimum number of remaining legal values
    mrv_cell = min(empty_cells, key=domain_size)
    
    return mrv_cell

def get_possible_values(board, row, col):
    """This function returns the domain of a cell"""
    # initialize an empty set to store the values in same row, column, and subgrid
    current_values = set()
    
    # store values in the same row and column
    for i in range(9):
        current_values.add(board[row + COL[i]])
        current_values.add(board[ROW[i] + col])
    
    # store values in the same 3x3 subgrid
    subgrid_start_row, subgrid_start_col = 3 * (ROW.index(row) // 3), 3 * (COL.index(col) // 3)
    for i in range(subgrid_start_row, subgrid_start_row + 3):
        for j in range(subgrid_start_col, subgrid_start_col + 3):
            current_values.add(board[ROW[i] + COL[j]])
    
    # domain is possible values (1-9) not already in current values
    domain = set(range(1, 10)) - current_values
    
    return domain

    
def forward_checking(board, row, col, value):
    """Check if the domain of cells in same row, column, and subgrid are empty"""
    empty_cells = get_empty_cells(board)

    # check domain of empty cells in same row and column
    for cell in empty_cells:
        r, c = cell
        if r == row or c == col and board[r + c] == 0:

        # domain is empty after removing the value, so current assignment is invalid
            if len(get_possible_values(board, r, c) - {value}) == 0:
                return False
    
    # check domain of empty cells in same 3x3 subgrid
    for i in range(3 * (ROW.index(row) // 3), 3 * (ROW.index(row) // 3) + 3):
        for j in range(3 * (COL.index(col) // 3), 3 * (COL.index(col) // 3) + 3):
            if board[ROW[i] + COL[j]] == 0:

                # domain is empty after removing the value, so current assignment is invalid
                if len(get_possible_values(board, ROW[i], COL[j]) - {value}) == 0:
                    return False
    
    return True
    

def backtracking(board):
    """Performs backtracking search. States are updated by directly modifying the board's dictionary."""
    empty_cells = get_empty_cells(board)
    if not empty_cells:
        return board  # board is solved
    row, col = mrv_heuristic(board) # find the cell with the smallest domain
    
    # perform forward checking on each possible value for the cell
    for value in get_possible_values(board, row, col):
        board[row + col] = value
        if forward_checking(board, row, col, value):
            result = backtracking(board)
            if result:
                return result
        board[row + col] = 0  # Delete assignment if failure is received
    return False


if __name__ == '__main__':
    # #  Read boards from source.
    # src_filename = 'sudokus_start.txt'
    # try:
    #     srcfile = open(src_filename, "r")
    #     sudoku_list = srcfile.read()
    # except:
    #     print("Error reading the sudoku file %s" % src_filename)
    #     exit()

    if len (sys.argv) < 2:
        print("Usage: python driver_3.py <input_string>")
        sys.exit(1)
    
    # Get the input string from command line argument
    input_string = sys.argv[1]

    if len(input_string) < 81:
        print("Puzzle needs to be input as 81 integers with 0 representing blank")

    # Parse the input string to create the board
    board = { ROW[r] + COL[c]: int(input_string[9*r+c])
              for r in range(9) for c in range(9)}
    
    start_time = time.time()
    # Solve with backtracking
    solved_board = backtracking(board)
    running_time = time.time() - start_time

    # Setup output file
    out_filename = 'output.txt'
    outfile = open(out_filename, "w")

    # start_time = time.time()
    # # Solve each board using backtracking
    # for line in sudoku_list.split("\n"):

    #     if len(line) < 9:
    #         continue

    #     # Parse boards to dict representation, scanning board L to R, Up to Down
    #     board = { ROW[r] + COL[c]: int(line[9*r+c])
    #               for r in range(9) for c in range(9)}

    # # # Print starting board. TODO: Comment this out when timing runs.
    # # print_board(board)
    
    #     # Solve with backtracking
    #     solved_board = backtracking(board)


    # # # Print solved board. TODO: Comment this out when timing runs.
    # # print_board(solved_board)

    #     # Write board to file
    #     outfile.write(board_to_string(solved_board))
    #     outfile.write('\n')

    # running_time = time.time() - start_time
    print("Running time: {:.4f} seconds".format(running_time))


    # Print starting board. TODO: Comment this out when timing runs.
    print_board(board)

    # Print solved board. TODO: Comment this out when timing runs.
    print_board(solved_board)

    # Write board to file
    outfile.write(board_to_string(solved_board))
    outfile.write('\n')

    print("Finishing all boards in file.")