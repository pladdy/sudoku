import io
import pytest
import sys

import sudoku.grid as grid


class TestGrid:
    def test_grid(self):
        g = grid.Grid()
        assert g.grid_type == "grid"

    def test_grid_add_row(self):
        g = grid.Grid()
        row = [7, 0, 9, 4, 0, 2, 3, 8, 0]
        g.add_row(row)
        g.add_row(row)
        assert g.rows == [row, row]

    def test_grid_add_row_exceptions(self):
        g = grid.Grid()

        tests = [None, "foo", 1, {"a": 4}, {3, 4, 5}, (3, 4, 5)]
        for test in tests:
            with pytest.raises(TypeError):
                g.add_row(test)

        tests = [[1], [1, 2, 3, 4, 5, 6, 7, 8, 8], [1, 2, 3, 4, 5, 6, 7, 10, 8]]
        for test in tests:
            with pytest.raises(ValueError):
                g.add_row(test)

        with pytest.raises(RuntimeError):
            # modify the row count internally to quickly verify you can't
            # add more than 9 rows
            g.rows = [[], [], [], [], [], [], [], [], []]
            g.add_row([1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_grid_show(self):
        _sysout = sys.stdout
        sys.stdout = result = io.StringIO()

        g = grid.Grid()
        g.add_row([1, 2, 3, 4, 5, 6, 7, 8, 9])
        g.show()

        sys.stdout = _sysout
        assert result.getvalue() == "[1, 2, 3, 4, 5, 6, 7, 8, 9]\n"

    def test_grid_solve(self):
        g = grid.Grid()
        g.add_row([0, 5, 4, 9, 6, 0, 0, 3, 8])
        g.add_row([0, 0, 0, 0, 0, 0, 4, 0, 0])
        g.add_row([7, 0, 2, 3, 5, 4, 0, 6, 9])
        g.add_row([0, 7, 0, 0, 9, 3, 0, 0, 0])
        g.add_row([4, 0, 0, 0, 0, 0, 0, 0, 2])
        g.add_row([0, 0, 0, 6, 2, 0, 0, 4, 0])
        g.add_row([6, 4, 0, 1, 8, 9, 3, 0, 5])
        g.add_row([0, 0, 3, 0, 0, 0, 0, 0, 0])
        g.add_row([8, 2, 0, 0, 3, 5, 6, 9, 0])

        g.solve()

        assert g.rows[0] == [1, 5, 4, 9, 6, 7, 2, 3, 8]
        assert g.rows[1] == [3, 6, 9, 8, 1, 2, 4, 5, 7]
        assert g.rows[2] == [7, 8, 2, 3, 5, 4, 1, 6, 9]
        assert g.rows[3] == [2, 7, 8, 4, 9, 3, 5, 1, 6]
        assert g.rows[4] == [4, 3, 6, 5, 7, 1, 9, 8, 2]
        assert g.rows[5] == [9, 1, 5, 6, 2, 8, 7, 4, 3]
        assert g.rows[6] == [6, 4, 7, 1, 8, 9, 3, 2, 5]
        assert g.rows[7] == [5, 9, 3, 2, 4, 6, 8, 7, 1]
        assert g.rows[8] == [8, 2, 1, 7, 3, 5, 6, 9, 4]

    def test_grid_solve_unsolvable(self):
        g = grid.Grid()
        g.add_row([7, 0, 9, 4, 0, 2, 3, 8, 0])
        g.add_row([6, 0, 3, 0, 0, 0, 0, 5, 0])
        g.add_row([0, 8, 0, 0, 0, 5, 0, 0, 0])
        g.add_row([0, 0, 4, 2, 1, 8, 0, 9, 0])
        g.add_row([0, 0, 0, 6, 0, 4, 0, 0, 0])
        g.add_row([0, 7, 0, 5, 3, 9, 4, 0, 0])
        g.add_row([0, 0, 0, 1, 0, 0, 0, 4, 0])
        g.add_row([0, 9, 0, 0, 0, 0, 5, 0, 3])
        g.add_row([0, 4, 5, 9, 0, 7, 1, 0, 8])

        with pytest.raises(Exception):
            g.solve()

    def test_grid_solved(self):
        g = grid.Grid()
        g.add_row([7, 0, 9, 4, 0, 2, 3, 8, 0])
        g.add_row([6, 0, 3, 0, 0, 0, 0, 5, 0])
        g.add_row([0, 8, 0, 0, 0, 5, 0, 0, 0])
        g.add_row([0, 0, 4, 2, 1, 8, 0, 9, 0])
        g.add_row([0, 0, 0, 6, 0, 4, 0, 0, 0])
        g.add_row([0, 7, 0, 5, 3, 9, 4, 0, 0])
        g.add_row([0, 0, 0, 1, 0, 0, 0, 4, 0])
        g.add_row([0, 9, 0, 0, 0, 0, 5, 0, 3])
        g.add_row([0, 4, 5, 9, 0, 7, 1, 0, 8])

        assert g.solved() is False


def test_validate_row():
    tests = [None, "foo", 1, {"a": 4}, {3, 4, 5}, (3, 4, 5)]
    for test in tests:
        with pytest.raises(TypeError):
            grid.validate_row(test)

    tests = [[1], [1, 2, 3, 4, 5, 6, 7, 8, 8], [1, 2, 3, 4, 5, 6, 7, 10, 8]]
    for test in tests:
        with pytest.raises(ValueError):
            grid.validate_row(test)
