MAX_ARRAY_COUNT = MAX_ROWS = 9
MAX_ARRAY_SUM = 45
COMPLETE_ARRAY = {1, 2, 3, 4, 5, 6, 7, 8, 9}


class Grid:
    def __init__(self):
        self.grid_type = "grid"
        self.rows = []
        self.columns = [[], [], [], [], [], [], [], [], []]

    def add_row(self, numbers):
        self.validate_array(numbers)
        if len(self.rows) >= MAX_ROWS:
            raise RuntimeError("Grid is full: no more rows can be added")

        self.columns.append([])
        for i, val in enumerate(numbers):
            self.columns[i].append(val)

        self.rows.append(numbers)

    def show(self):
        for row in self.rows:
            print(row)

    def validate_array(self, numbers):
        if type(numbers).__name__ != "list":
            raise TypeError("Invalid argument, must be a list")
        if len(numbers) != MAX_ARRAY_COUNT:
            raise ValueError("Invalid array: too many numbers")
        if len(set(numbers)) != len(numbers):
            raise ValueError("Invalid row: row has duplicate numbers")
        if sum(numbers) > MAX_ARRAY_SUM:
            raise ValueError("Invalid row: row total is too high")


# TODO: inheritance vs composition; when a grid is made, create subgrids?
class SubGrid(Grid):
    def __init__(self):
        self.grid_type = "subgrid"
