# Sudoku Solver Instructions

## Part 1 and Backtrack Testing

To see the answer to Part 1 and Backtrack testing, run `program2.py`.

## Testing on Other Puzzles

To test on other puzzles, follow these steps:

1. Pass a list into the `Sudoku` class constructor:

    ```python
    sudoku_example = Sudoku(List[int])
    ```

2. Set the constraints by copying the `constraint9x9`:

    ```python
    sudoku_example.constraints = copy.deepcopy(constraint9x9)
    ```

3. Set adjacency of each cell:

    ```python
    sudoku_example.init_adjacency()
    ```

## Running the Website

1. Run the backend server by executing `backend.py`.
   
2. Open `web.html` in a browser (preferably Chrome).

3. Ensure that on line 538 of `web.html`, the URL matches up with the Python Flask URL.

4. Input a Sudoku puzzle into the provided input field.

5. Press the "Solve" button to solve the Sudoku.

6. Use the buttons <<, <, >, >> to navigate through the steps leading to the solution (no steps, back, next, last step respectively).
