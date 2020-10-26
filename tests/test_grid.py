import io
import pytest
import sys

import sudoku.grid as grid


class TestGrid:
    def test_grid(self):
        g = grid.Grid()
        assert g.grid_type == "grid"

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

    def test_grid_validate_array(self):
        g = grid.Grid()

        tests = [None, "foo", 1, {"a": 4}, {3, 4, 5}, (3, 4, 5)]
        for test in tests:
            with pytest.raises(TypeError):
                g.validate_array(test)

        tests = [[1], [1, 2, 3, 4, 5, 6, 7, 8, 8], [1, 2, 3, 4, 5, 6, 7, 10, 8]]
        for test in tests:
            with pytest.raises(ValueError):
                g.validate_array(test)


def test_subgrid():
    g = grid.SubGrid()
    assert g.grid_type == "subgrid"
