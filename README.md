# Sudoku Solver

## Description
This Python program solves the sudoku puzzles using backtracking with inference.

## Usage
Run the program and provide a Sudoku puzzle in the form of a string of 81 integers. Use 0s to represent blanks.

## Example
### Input:

python driver_3.py 800000000003600000070090200050007000000045700000100030001000068008500010090000400


### Output:

812753649943682175675491283154237896369845721287169534521974368438526917796318452

## Implementation Details
- The program uses backtracking with inference (forward checking) to solve Sudoku puzzles.
- The Minimum Remaining Values (MRV) selects the empty cell with the fewest remaining legal values as the next cell to assign a value to. This is applied at each step of the backtracking algorithm to reduce the search space.
- The solution is written to an output file named `output.txt`.

## Version used
- Python 3.11.6

## Remarks
- The program has a running time of approximately 35 seconds to complete 400 puzzles and write them to a file.
- All 400 puzzles in the input text files were solved correctly and matched the solutions in the provided `sudokus_finish.txt` file.
- The most difficult Sudoku puzzle was solved in about 0.24 seconds.