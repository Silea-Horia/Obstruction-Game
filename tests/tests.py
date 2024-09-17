import unittest

from src.domain.cell import Cell
from src.services.services import Services


class TestCell(unittest.TestCase):
    def test_create_cell(self):
        test_cell = Cell()
        assert test_cell.state == 0
        assert test_cell.sign == " "

        test_cell.block()
        assert test_cell.state == 1

        state = 1
        test_cell = Cell(state)
        assert test_cell.state == 1

        test_cell.block()
        assert test_cell.state == 1

        try:
            test_cell = Cell("not good")
        except ValueError as ve:
            assert str(ve) == "State must be an int!"

        try:
            test_cell = Cell(2)
        except ValueError as ve:
            assert str(ve) == "State must be either 0 or 1!"

        test_cell = Cell()

        test_cell.set_sign("O")
        assert test_cell.sign == "O"

        test_cell.set_sign("X")
        assert test_cell.sign == "X"

        try:
            test_cell.set_sign(134)
        except ValueError as ve:
            assert str(ve) == "Sign must be a string!"

        try:
            test_cell.set_sign("bad")
        except ValueError as ve:
            assert str(ve) == "Sign must be either O or X!"

    def test_services(self):
        services = Services()
        assert services.board == [[]]

        lines = 2
        columns = 3
        services.create_board(lines, columns)
        assert len(services.board) == lines
        assert len(services.board[0]) == columns

        lines = -1
        try:
            services.create_board(lines, columns)
        except ValueError as ve:
            assert str(ve) == "Sizes must be non-zero positive integers!"

        assert services.empty_space() is True

        lines = 1
        columns = 1
        services.create_board(lines, columns)
        services.mark_cell("1", "1", "O")
        assert services.empty_space() is not True

        try:
            services.mark_cell("1", "2", "O")
        except ValueError as ve:
            assert str(ve) == "Column index must be between 1 and 1!"

        try:
            services.mark_cell("1", "1", "O")
        except ValueError as ve:
            assert str(ve) == "The selected cell is blocked!"

if __name__ == '__main__':
    unittest.main()
