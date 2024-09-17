from src.domain.cell import Cell


class Services:
    def __init__(self, board=None):
        if board is None:
            board = [[]]
            self.__lines = 0
            self.__columns = 0
        else:
            self.__lines = len(board)
            self.__columns = len(board[0])
        self.__board = board

    def blank_spots(self) -> int:
        """
        Function that counts the number of open cells in the board
        :return: The number of open cells of the board
        """
        count = 0
        for line in self.__board:
            for cell in line:
                if cell.state == 0:
                    count += 1
        return count

    def create_board(self, lines: int, columns: int):
        """
        Function that creates a matrix of empty cells with dimensions lines and columns
        :param lines: Number of lines
        :param columns: Number of columns
        :raise: ValueError if the number of lines or columns are less or equal to zero
        :return: NoneType
        """
        if lines < 1 or columns < 1:
            raise ValueError("Sizes must be non-zero positive integers!")
        self.__lines = lines
        self.__columns = columns
        self.__board = [[]]
        for i in range(lines):
            for j in range(columns):
                self.__board[i].append(Cell())
            self.__board.append([])
        self.__board.pop()      # get rid of last, unused list

    @property
    def board(self):
        return self.__board

    def __validate_coordinates(self, line: int, column: int):
        """
        Function that checks if the provided coordinates fit in the current matrix
        and if the selected cell is not marked
        :param line: The line index
        :param column: The column index
        :raise: ValueError if the indexes are outside the matrix or if the selected cell is marked
        :return: NoneType
        """
        if line < 0 or line >= self.__lines:
            raise ValueError(f"Line index must be between 1 and " + str(self.__lines) + "!")
        if column < 0 or column >= self.__columns:
            raise ValueError(f"Column index must be between 1 and " + str(self.__columns) + "!")
        if self.__board[line][column].state == 1:
            raise ValueError("The selected cell is blocked!")

    def mark_cell(self, line: str, column: str, sign: str):
        """
        Function that marks a cell and all adjacent cells, if they exist
        :param line: The line index
        :param column: The column index
        :param sign: The sign of the player marking the cell
        :return: NoneType
        """
        line = int(line)-1      # lines in the matrix are 0 indexed, while the player provides a 1 indexed number
        column = int(column)-1
        self.__validate_coordinates(line, column)

        # block selected cell and put the sign of the player
        self.__board[line][column].block()
        self.__board[line][column].set_sign(sign)

        # block the cells around it
        if line > 0:
            self.__board[line-1][column].block()
            if column > 0:
                self.__board[line-1][column-1].block()
            if column < self.__columns - 1:
                self.__board[line-1][column+1].block()
        if line < self.__lines - 1:
            self.__board[line+1][column].block()
            if column > 0:
                self.__board[line+1][column-1].block()
            if column < self.__columns - 1:
                self.__board[line+1][column+1].block()
        if column > 0:
            self.__board[line][column - 1].block()
        if column < self.__columns - 1:
            self.__board[line][column + 1].block()

    def empty_space(self) -> bool:
        """
        Function that checks if the board has any open cells
        :return: True if there is at least one open cell, False otherwise
        """
        for line in self.__board:
            for cell in line:
                if cell.state == 0:
                    return True
        return False
