MAX_ARRAY_COUNT = MAX_ROWS = 9
MAX_ARRAY_SUM = 45
COMPLETE_ARRAY = [1, 2, 3, 4, 5, 6, 7, 8, 9]
SUBGRIDS_BY_ROWS = [
    [0, 0, 0, 1, 1, 1, 2, 2, 2],
    [0, 0, 0, 1, 1, 1, 2, 2, 2],
    [0, 0, 0, 1, 1, 1, 2, 2, 2],
    [3, 3, 3, 4, 4, 4, 5, 5, 5],
    [3, 3, 3, 4, 4, 4, 5, 5, 5],
    [3, 3, 3, 4, 4, 4, 5, 5, 5],
    [6, 6, 6, 7, 7, 7, 8, 8, 8],
    [6, 6, 6, 7, 7, 7, 8, 8, 8],
    [6, 6, 6, 7, 7, 7, 8, 8, 8],
]

# TODO: What if each "cell" was an object, that contained it's row, column,
#       subgrid?


class Grid:
    """Provide instances of sudoku board/grids.

    The values in the board are stored in 3 attributes of the object.  The
    trade off, in theory, is by keeping the rows, columns, and subgrids
    duplicated, it should be more efficient to check if a board is solved.

    An alternative would be to store the board as a 2D array, and the concept
    of rows, columns, and subgrids can be calculated when checking for a cells'
    solution.  However given that each cell may have to be looked up multiple
    times I opted to triplicate the data...which feels gross.
    """

    def __init__(self):
        self.grid_type = "grid"
        self.rows = []
        self.columns = [[], [], [], [], [], [], [], [], []]
        self.subgrids = {}
        for i in range(9):
            self.subgrids[i] = []

    def add_row(self, numbers):
        """Add a row to the grid.

        Arguments:
            - list of positive integers, 1-9

        Returns: n/a

        Usage:
            g.add_row([1, 2, 3, 4, 5, 6, 7, 8, 9])
            g.add_row([1, 2, 3, 0, 0, 0, 7, 8, 9])

        Notes:
            - The list of numbers is validated and will be rejected if invalid.
                - Must have 9 digits
                - Can include multiple 0's for unknown cells
                - Any numbers in the range 1-9 must be unique
            - The grid is not checked to see if a row will make a board that's
              impossible to solve.
        """
        self.validate_row(numbers)
        if len(self.rows) >= MAX_ROWS:
            raise RuntimeError("Grid is full: no more rows can be added")

        row_number = len(self.rows)
        for col, val in enumerate(numbers):
            self.columns[col].append(val)
            self.subgrids[self._subgrid(row_number, col)].append(val)

        self.rows.append(numbers)

    # TODO: should this print() or return an array of arrays?
    def show(self):
        """Print the grid in its current state."""
        for row in self.rows:
            print(row)

    def solve(self):
        """Solve the sudoku puzzle.

        Arguments: n/a

        Returns: n/a

        Usage:
            g.solve()

        Notes:
            - This method will mutate the instance's attributes.  As it finds
              solutions to cells it will update accordingly.
            - If a puzzle can't be solved (the puzzle is iterated through with
              no changes), an exception is thrown to avoid an infinite loop.
        """
        while self.solved() is False:
            changes = 0
            for r, row in enumerate(self.rows):
                for c, val in enumerate(row):
                    if self.rows[r][c] == 0:
                        result = self._solve_cell(r, c)
                        if result > 0:
                            self._update_cell(r, c, result)
                            changes += 1

            if changes == 0:
                raise Exception("Puzzle is unsolvable")

    def solved(self):
        """Check if puzzle is solved.

        Arguments: n/a

        Returns:
            - bool, True or False
        """
        for row in self.rows:
            if sorted(row) != COMPLETE_ARRAY:
                return False

        for col in self.columns:
            if sorted(col) != COMPLETE_ARRAY:
                return False

        for subgrid in self.subgrids:
            if sorted(self.subgrids[subgrid]) != COMPLETE_ARRAY:
                return False

        return True

    def validate_row(self, numbers):
        """Given a row of numbers, verify it could be a sudoku row.

        Arguments:
            - list of integers

        Returns: n/a

        Notes:
            - A valid list
                - must be 9 numbers.
                - each number must be between 0-9.
                - 0's can be repeated in the list.
                - numbers 1-9 must be unique
            - If a row is invalid, an exception is thrown.
        """
        if type(numbers).__name__ != "list":
            raise TypeError("Invalid argument, must be a list")
        if len(numbers) != MAX_ARRAY_COUNT:
            raise ValueError("Invalid array: too many numbers")

        no_zeros = self._filter_zeros(numbers)
        if len(set(no_zeros)) != len(no_zeros):
            raise ValueError("Invalid row: row has duplicate numbers")
        if sum(numbers) > MAX_ARRAY_SUM:
            raise ValueError("Invalid row: row total is too high")

    def _filter_zeros(self, xs):
        """Return a list of numbers with 0s removed from the list"""
        return list(filter(lambda x: x != 0, xs))

    def _solve_cell(self, r, c):
        """Given a cell (row, column), try to identify it's correct value

        Arguments:
            - row, integer
            - column, integer

        Returns:
            - value, integer

        Details:
            - Row and column correspond to a row and column in the puzzle.
            - The check is to try and find a unique integer not yet used in
                - the row
                - the column
                - and the subgrid
        """
        subgrid = self.subgrids[self._subgrid(r, c)]
        row = self.rows[r]
        col = self.columns[c]
        available = set.difference(
            set(COMPLETE_ARRAY), set(subgrid), set(row), set(col)
        )

        if len(available) == 1:
            return available.pop()
        return 0

    def _subgrid(self, r, c):
        """Given a row/col coordinate, identify which subgrid it's in"""
        return SUBGRIDS_BY_ROWS[r][c]

    # TODO: we store the same data 3 ways...I wonder if there's a way to do this
    #       just once to make updating easier?
    def _update_cell(self, r, c, val):
        """Given a row/col coordinate and value, update the grid with the value.

        Arguments:
            - row, integer
            - column, integer

        Returns: n/a

        Details:
            - Since the instance tracks rows, columns, and subgrids separately
              this method is used to keep them updated so they're in sync.
        """
        self.rows[r][c] = val
        self.columns[c][r] = val

        subgrid = self.subgrids[self._subgrid(r, c)]
        subgrid_index = (r % 3) * 3 + c % 3
        subgrid[subgrid_index] = val
